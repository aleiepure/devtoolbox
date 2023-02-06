# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import abc
from gi.repository import Gio, GObject
from typing import List


class Formatter(abc.ABC):

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _format_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._format(self._text, self._indentations)
        task.return_value(outcome)

    def format_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._format_thread)

    def format_async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        return result.propagate_value().value

    def set_input(self, text:str):
        self._text = text

    def set_indentations(self, indents:int):
        self._indentations = indents

    def get_cancellable(self):
        return self._cancellable

    @abc.abstractmethod
    def _format(self, text:str, indents:int):
        pass

    @abc.abstractmethod
    def is_correct(self, text:str) -> bool:
        pass

    @abc.abstractmethod
    def get_title(self) -> str:
        pass

    @abc.abstractmethod
    def get_description(self) -> str:
        pass

    @abc.abstractmethod
    def get_utility_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_textarea_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_language(self) -> str:
        pass

    @abc.abstractmethod
    def get_file_extensions(self) -> List[str]:
        pass
