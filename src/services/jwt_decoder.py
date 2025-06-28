# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
import json
import base64
import jwt


class JwtDecoderService:

    def __init__(self):
        self._cancellable = Gio.Cancellable()
        self._token = None
        self._private_key = None
        self._public_key = None
        self._header = None
        self._payload = None

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

    def _verify_signature_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._verify_signature(self._token, self._public_key)
        task.return_value(outcome)

    def _encode_token_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._encode_token(self._header, self._payload, self._private_key)
        task.return_value(outcome)

    @staticmethod
    def _decode_header(token:str) -> str:
        return json.dumps(jwt.get_unverified_header(token), indent=4, ensure_ascii=False)

    @staticmethod
    def _decode_payload(token:str) -> str:
        return json.dumps(jwt.decode(token, options={"verify_signature": False}), indent=4, ensure_ascii=False)

    @staticmethod
    def _verify_signature(token:str, key:str|bytes) -> bool:
        try:
            jwt.decode(token, key,
                       algorithms=[jwt.get_unverified_header(token)["alg"]],
                       options={
                "verify_signature": True,
                "verify_aud": False,
                "verify_iss": False,
                "verify_exp": False,
                "verify_iat": False,
                "verify_nbf": False
            })
            return True
        except (jwt.exceptions.PyJWTError, KeyError, NotImplementedError):
            return False

    @staticmethod
    def _encode_token(header:str, payload:str, key:str|bytes|None) -> str | None:
        header = json.loads(header)
        payload = json.loads(payload)
        if key is None:
            encoded = ""
            for item in (header, payload):
                encoded += base64.urlsafe_b64encode(
                    json.dumps(
                        item, ensure_ascii=False, separators=(',', ':')
                    ).encode("utf-8")
                ).decode("utf-8").rstrip("=") + "."
            return encoded
        elif "alg" in header and header["alg"] == "none":
            key = None

        try:
            return jwt.encode(payload=payload,
                              headers=header,
                              key=key)
        except (jwt.exceptions.PyJWTError, KeyError, NotImplementedError):
            return None

    def decode_header_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decode_header_thread)

    def decode_payload_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decode_payload_thread)

    def verify_signature_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._verify_signature_thread)

    def encode_token_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._encode_token_thread)

    @staticmethod
    def task_finish(result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return None
        return result.propagate_value().value

    def set_token(self, token:str):
        self._token = token

    def set_payload(self, payload:str):
        self._payload = payload

    def set_header(self, header:str):
        self._header = header

    def set_private_key(self, key:str|bytes|None):
        self._private_key = key

    def set_public_key(self, key:str|bytes|None):
        self._public_key = key

    def get_cancellable(self):
        return self._cancellable
