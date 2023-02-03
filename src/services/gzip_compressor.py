# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from typing import List
import base64
import binascii
import gzip


class GzipCompressorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _compress_text_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._compress_text(self._input)
        task.return_value(outcome)

    def _compress_bytes_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._compress_bytes(self._input)
        task.return_value(outcome)

    def _decompress_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decompress(self._input)
        task.return_value(outcome)

    def _compress_text(self, input:str):
        return base64.b64encode(gzip.compress(input.encode("utf-8"))).decode("utf-8")

    def _compress_bytes(self, input:List[bytes]):
        return base64.b64encode(gzip.compress(input)).decode("utf-8")

    def _decompress(self, input:str):
        try:
            return gzip.decompress(base64.b64decode(input))
        except binascii.Error:
            return ""

    def compress_text_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._compress_text_thread)

    def compress_bytes_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._compress_bytes_thread)

    def decompress_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decompress_thread)

    def async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input(self, input_text_or_bytes):
        self._input = input_text_or_bytes
