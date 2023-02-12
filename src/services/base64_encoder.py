# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject, Gtk, Gdk
from typing import List
from base64io import Base64IO
from pathlib import Path
import base64
import binascii


class Base64EncoderService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _encode_text_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._encode_text(self._input)
        task.return_value(outcome)

    def _encode_file_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._encode_file(self._input)
        task.return_value(outcome)

    def _decode_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decode(self._input)
        task.return_value(outcome)

    def _encode_text(self, text:str) -> str:
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def _encode_file(self, input_file_path:str) -> str:
        output_file_path = Gio.File.new_tmp("me.iepure.devtoolbox.XXXXXX")[0].get_path()
        print(output_file_path)

        with open(input_file_path, "rb") as source, open(output_file_path, "wb") as target:
            with Base64IO(target) as encoded_target:
                for line in source:
                    encoded_target.write(line)
                    print(".", end="")

        txt = Path(output_file_path).read_text()
        if txt[len(txt)-1] != '\x00':
            txt += '\x00'

        return txt

    def _decode(self, text):


        try:
            return base64.b64decode(text)
        except binascii.Error:
            return ""

    def encode_text_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._encode_text_thread)

    def encode_file_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._encode_file_thread)

    def decode_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decode_thread)

    def async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input(self, input_text_or_bytes):
        self._input = input_text_or_bytes
