# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Literal
from gi.repository import Gio, GObject
import base64
import binascii
import gzip
import lzma
import bz2
from io import BytesIO


class CompressionService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()
        self._compression_type = "gzip"

    # MARK: -- Threads
    def _compress_text_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._compress_text(self._input)
        task.return_value(outcome)

    def _compress_bytes_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._compress_bytes(self._input)
        task.return_value(outcome)

    def _decompress_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decompress(self._input)
        task.return_value(outcome)

    # MARK: -- Compression and Decompression Methods
    def _compress_text(self, input_str: str):
        data = input_str.encode("utf-8")
        if self._compression_type == "gzip":
            compressed = gzip.compress(data)
        elif self._compression_type == "lzma":
            compressed = lzma.compress(data)
        elif self._compression_type == "bz2":
            compressed = bz2.compress(data)
        else:
            raise ValueError(
                f"Unsupported compression type: {self._compression_type}")

        return base64.b64encode(compressed).decode("utf-8")

    def _compress_bytes(self, input_file_path: str):
        with open(input_file_path, "rb") as input_file:
            data = input_file.read()

        if self._compression_type == "gzip":
            with BytesIO() as buffer:
                with gzip.GzipFile(fileobj=buffer, mode='wb') as comp_file:
                    comp_file.write(data)
                compressed_data = buffer.getvalue()
        elif self._compression_type == "lzma":
            compressed_data = lzma.compress(data)
        elif self._compression_type == "bz2":
            compressed_data = bz2.compress(data)
        else:
            raise ValueError(
                f"Unsupported compression type: {self._compression_type}")

        return base64.b64encode(compressed_data).decode("utf-8")

    def _decompress(self, input_str: str):
        try:
            decoded_data = base64.b64decode(input_str.encode())
            
            if self._compression_type == "gzip":
                with gzip.open(BytesIO(decoded_data), 'rb') as comp_file:
                    decompressed_data = comp_file.read()
            elif self._compression_type == "lzma":
                decompressed_data = lzma.decompress(decoded_data)
            elif self._compression_type == "bz2":
                decompressed_data = bz2.decompress(decoded_data)
            else:
                raise ValueError(f"Unsupported compression type: {self._compression_type}")
                
            return decompressed_data
        except (binascii.Error, lzma.LZMAError, OSError):
            return ""

    # MARK: -- Async Methods
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

    def async_finish(self, result: Gio.AsyncResult, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._input = None
        return result.propagate_value().value

    # MARK: -- Getters and Setters
    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input(self, input_text_or_bytes):
        self._input = input_text_or_bytes

    def set_compression_type(self, compression_type: Literal["gzip", "lzma", "bz2"]):
        self._compression_type = compression_type
