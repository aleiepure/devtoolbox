# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject, Gcr
from asn1crypto import pem


class CertificateParserService:

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_path(self, path:str):
        self._path = path

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def get_gcr_async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._path = None
        return result.propagate_value().value

    def get_gcr_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._get_gcr_thread)

    def _get_gcr_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._get_gcr(self._path)
        task.return_value(outcome)

    def _get_gcr(self, path:str):
        with open(path, "rb") as f:
            file_bytes = f.read()
            if pem.detect(file_bytes):
                _, _, file_bytes = pem.unarmor(file_bytes)
            return Gcr.SimpleCertificate.new(file_bytes)
