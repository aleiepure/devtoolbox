# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
import base64
import binascii
import gzip
from io import BytesIO


class GzipCompressorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _compress_text_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._compress_text(self._input)
        task.return_value(outcome)

    def _compress_bytes_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._compress_bytes(self._input)
        task.return_value(outcome)

    def _decompress_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decompress(self._input)
        task.return_value(outcome)

    def _compress_text(self, input_str:str):
        return base64.b64encode(gzip.compress(input_str.encode("utf-8"))).decode("utf-8")

    # def _compress_bytes(self, input_file_path:str):
    #     output_file_path = Gio.File.new_tmp("me.iepure.devtoolbox.XXXXXX")[0].get_path()
    #     with gzip.open(output_file_path, 'wb') as zip_file, open(input_file_path, "rb") as input_file:
    #         zip_file.write(input_file.read())

    #     with gzip.open(output_file_path, 'rb') as zip_file:
    #         return base64.b64encode(zip_file.read()).decode("utf-8")
    
    def _compress_bytes(self, input_file_path: str):
        with open(input_file_path, "rb") as input_file:
            with BytesIO() as gzip_buffer:
                with gzip.GzipFile(fileobj=gzip_buffer, mode='wb') as zip_file:
                    zip_file.write(input_file.read())
                
                # Get the compressed data and encode it in base64
                compressed_data = gzip_buffer.getvalue()
                encoded_data = base64.b64encode(compressed_data).decode("utf-8")

        return encoded_data

    def _decompress(self, input_str:str):
        try:
            decoded_data = base64.b64decode(input_str.encode())
            with gzip.open(BytesIO(decoded_data), 'rb') as zip_file:
                decompressed_data = zip_file.read()
                return decompressed_data
        except binascii.Error:
            return ""

    def compress_text_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._compress_text_thread)

    def compress_bytes_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._compress_bytes_thread)

    def decompress_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decompress_thread)

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._input = None
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input(self, input_text_or_bytes):
        self._input = input_text_or_bytes
