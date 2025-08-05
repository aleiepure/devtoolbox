# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import binascii
from typing import Callable
from gi.repository import Gio, GObject, GLib

from ..compressors.compressor import Compressor


class CompressorService():

    def __init__(self, compressor: Compressor):
        self._compressor = compressor
        self._cancellable = None
        self._input = ""

    # MARK: -- Threads
    def _compress_text_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        try:
            if cancelable.is_cancelled():
                return
            result = self._compressor.compress_text(self._input)
            task.return_value(GObject.Value(str, result))
        except Exception as e:
            task.return_error(GLib.Error(f"Compression failed: {str(e)}"))

    def _compress_bytes_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        try:
            if cancelable.is_cancelled():
                return
            with open(self._input, "rb") as input_file:
                data = input_file.read()
            result = self._compressor.compress_bytes(data)
            task.return_value(GObject.Value(str, result))
        except Exception as e:
            task.return_error(GLib.Error(f"Compression failed: {str(e)}"))

    def _decompress_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        try:
            if cancelable.is_cancelled():
                return
            result = self._compressor.decompress(self._input)

            if isinstance(result, bytes):
                task.return_value(GObject.Value(GLib.Bytes, GLib.Bytes(result)))
            else:
                task.return_value(GObject.Value(str, str(result)))

        except (binascii.Error, Exception) as e:
            task.return_error(GLib.Error(f"Decompression failed: {str(e)}"))

    # MARK: -- Async Methods
    def compress_text_async(self, source_object: GObject.Object, callback: Callable, user_data: object = None):
        self._cancellable = Gio.Cancellable()
        task = Gio.Task.new(
            source_object, self._cancellable, callback, user_data)
        task.run_in_thread(self._compress_text_thread)

    def compress_bytes_async(self, source_object: GObject.Object, callback: Callable, user_data: object = None):
        self._cancellable = Gio.Cancellable()
        task = Gio.Task.new(
            source_object, self._cancellable, callback, user_data)
        task.run_in_thread(self._compress_bytes_thread)

    def decompress_async(self, source_object: GObject.Object, callback: Callable, user_data: object = None):
        self._cancellable = Gio.Cancellable()
        task = Gio.Task.new(
            source_object, self._cancellable, callback, user_data)
        task.run_in_thread(self._decompress_thread)

    def async_finish(self, result: Gio.AsyncResult, source_object: GObject.Object):
        if not Gio.Task.is_valid(result, source_object):
            return ""

        try:
            return result.propagate_value().value
        except GLib.Error as e:
            if e.code == Gio.IOErrorEnum.CANCELLED:
                return ""
            raise e

    # MARK: -- Getters and Setters
    def set_input(self, input_data: str):
        self._input = input_data

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable if self._cancellable else Gio.Cancellable()
