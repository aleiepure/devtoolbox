# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from ruamel import yaml
import json


class JsonYamlService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _convert_json_to_yaml_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_json_to_yaml(self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_yaml_to_json_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_yaml_to_json(self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_json_to_yaml(self, json_str: str, indents: int) -> str:
        return yaml.dump(
            json.loads(json_str),
            indent=indents,
            default_flow_style=False
        )

    def _convert_yaml_to_json(self, yaml_str:str, indents: int) -> str:
        return json.dumps(
            yaml.load(yaml_str, Loader=yaml.Loader),
            indent=indents,
            ensure_ascii=False
        )

    def convert_json_to_yaml_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_json_to_yaml_thread)

    def convert_yaml_to_json_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_yaml_to_json_thread)

    def convert_async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input_string(self, input: str):
        self._input_string = input

    def set_input_indents(self, indents: int=4):
        self._input_indents = indents
