# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from io import StringIO
from gi.repository import Gio, GObject
import ruamel.yaml
import json
import tomllib
import tomli_w

import datetime


class ExtendedJSONEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime.datetime):
            return value.timestamp()
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, ruamel.yaml.comments.CommentedSet):
            return list(value)
        return super().default(value)

# MARK: Service


class JsonYamlTomlService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    # MARK: -- Threads
    def _convert_json_to_yaml_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_json_to_yaml(
            self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_yaml_to_json_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_yaml_to_json(
            self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_json_to_toml_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_json_to_toml(self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_toml_to_json_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_toml_to_json(
            self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_yaml_to_toml_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_yaml_to_toml(self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_toml_to_yaml_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_toml_to_yaml(
            self._input_string, self._input_indents)
        task.return_value(outcome)

    # MARK: -- Conversions
    def _convert_json_to_yaml(self, json_str: str, indents: int) -> str:
        yaml = ruamel.yaml.YAML(typ=['rt'])
        yaml.indent(mapping=indents, sequence=indents, offset=indents)
        stream = StringIO()
        yaml.dump(json.loads(json_str), stream)
        return stream.getvalue()

    def _convert_yaml_to_json(self, yaml_str: str, indents: int) -> str:
        yaml = ruamel.yaml.YAML(typ='rt')

        return json.dumps(
            yaml.load(yaml_str),
            indent=indents,
            ensure_ascii=False,
            cls=ExtendedJSONEncoder,
        )

    def _convert_json_to_toml(self, json_str: str, indents: int) -> str:
        data = json.loads(json_str)
        cleaned_data = self._remove_null_values(data)
        return tomli_w.dumps(cleaned_data, indent=indents)

    def _convert_toml_to_json(self, toml_str: str, indents: int) -> str:
        data = tomllib.loads(toml_str)
        return json.dumps(
            data,
            indent=indents,
            ensure_ascii=False,
            cls=ExtendedJSONEncoder,
        )

    def _convert_yaml_to_toml(self, yaml_str: str, indents: int) -> str:
        yaml = ruamel.yaml.YAML(typ='rt')
        data = yaml.load(yaml_str)
        cleaned_data = self._remove_null_values(data)
        return tomli_w.dumps(cleaned_data, indent=indents)

    def _convert_toml_to_yaml(self, toml_str: str, indents: int) -> str:
        data = tomllib.loads(toml_str)
        yaml = ruamel.yaml.YAML(typ='rt')
        yaml.indent(mapping=indents, sequence=indents, offset=indents)
        stream = StringIO()
        yaml.dump(data, stream)
        return stream.getvalue()

    # MARK: -- Async Methods
    def convert_json_to_yaml_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_json_to_yaml_thread)

    def convert_yaml_to_json_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_yaml_to_json_thread)

    def convert_json_to_toml_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_json_to_toml_thread)

    def convert_toml_to_json_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_toml_to_json_thread)

    def convert_yaml_to_toml_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_yaml_to_toml_thread)

    def convert_toml_to_yaml_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_toml_to_yaml_thread)

    def convert_async_finish(self, result: Gio.AsyncResult, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._input_string = None
        self._input_indents = None
        return result.propagate_value().value

    # MARK: -- Getters and Setters
    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input_string(self, input: str):
        self._input_string = input

    def set_input_indents(self, indents: int = 4):
        self._input_indents = indents

    # MARK: -- Helpers
    def _remove_null_values(self, data):
        if isinstance(data, dict):
            return {k: self._remove_null_values(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [self._remove_null_values(item) for item in data if item is not None]
        else:
            return data
