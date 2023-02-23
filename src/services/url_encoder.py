# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from urllib import parse

class UrlEncoderService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _encode_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._encode(self._input, self._space_as_plus)
        task.return_value(outcome)

    def _decode_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decode(self._input)
        task.return_value(outcome)

    def _encode(self, input_str:str, space_as_plus:bool) -> str:
        if space_as_plus:
            return parse.quote_plus(input_str, safe=":/?#[]@!$&'()*+,;=")

        return parse.quote(input_str, safe=":/?#[]@!$&'()*+,;=")

    def _decode(self, input_str:str) -> str:
        return parse.unquote_plus(input_str)

    def encode_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._encode_thread)

    def decode_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decode_thread)

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._input = None
        self._space_as_plus = None
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input(self, input_str:str):
        self._input = input_str

    def set_space_as_plus(self, space_as_plus:bool):
        self._space_as_plus = space_as_plus
