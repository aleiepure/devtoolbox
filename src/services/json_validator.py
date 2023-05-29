# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
import json
from jsonschema import validate, exceptions


class JsonValidatorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_json(self, json:str):
        self._json = json

    def set_schema(self, schema:str):
        self._schema = schema

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._json = None
        self._schema = None
        return result.propagate_value().value

    def check_json_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._check_json_thread)

    def _check_json_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._check_json(self._json, self._schema)
        task.return_value(outcome)

    def _check_json(self, json_str:str, schema_str:str):
        try:
            validate(instance=json.loads(json_str), schema=json.loads(schema_str))
            return True, None, None
        except exceptions.ValidationError as error:
            return False, error.message, None
        except exceptions.SchemaError as error:
            return False, None, error.message
