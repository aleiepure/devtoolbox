# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
import json
import jwt


class JwtDecoderService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _decode_header_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decode_header(self._token)
        task.return_value(outcome)

    def _decode_payload_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decode_payload(self._token)
        task.return_value(outcome)

    def _decode_header(self, token:str) -> str:
        return json.dumps(jwt.get_unverified_header(token), indent=4)

    def _decode_payload(self, token:str) -> str:
        return json.dumps(jwt.decode(token, options={"verify_signature": False}), indent=4)

    def decode_header_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decode_header_thread)

    def decode_payload_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decode_payload_thread)

    def decode_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._token = None
        return result.propagate_value().value

    def set_token(self, token:str):
        self._token = token

    def get_cancellable(self):
        return self._cancellable
