# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
import re


class TextInspectorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_text(self, text:str):
        self._text = text

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        return result.propagate_value().value

    def to_sentence_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_sentence_case_thread)

    def _to_sentence_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_sentence_case(self._text)
        task.return_value(outcome)

    def _to_sentence_case(self, text:str) -> str:

        output = ""
        newSentence = True

        for i in range(0, len(text)):

            if text[i] == '.' or text[i] == '?' or text[i] == '!' or text[i] == '\n':
                output += text[i]
                newSentence = True
                continue

            if text[i].isalnum():
                if newSentence:
                    output += text[i].upper()
                    newSentence = False
                else:
                    output += text[i].lower()
            else:
                output += text[i]

        return output

    def to_lower_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_lower_case_thread)

    def _to_lower_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_lower_case(self._text)
        task.return_value(outcome)

    def _to_lower_case(self, text:str) -> str:

        output = ""

        for i in range(0, len(text)):
            output += text[i].lower()

        return output

    def to_upper_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_upper_case_thread)

    def _to_upper_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_upper_case(self._text)
        task.return_value(outcome)

    def _to_upper_case(self, text:str) -> str:

        output = ""

        for i in range(0, len(text)):
            output += text[i].upper()

        return output

    def to_title_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_title_case_thread)

    def _to_title_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_title_case(self._text)
        task.return_value(outcome)

    def _to_title_case(self, text:str) -> str:

        output = ""

        for i in range(0, len(text)):
            if i == 0 or not text[i-1].isalnum():
                output += text[i].upper()
            else:
                output += text[i].lower()

        return output

    def to_camel_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_camel_case_thread)

    def _to_camel_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_camel_case(self._text)
        task.return_value(outcome)

    def _to_camel_case(self, text:str) -> str:

        output = ""
        next_uppercase = False

        for i in range(0, len(text)):
            if text[i].isalnum():
                if next_uppercase:
                    output += text[i].upper()
                    next_uppercase = False
                else:
                    output += text[i].lower()
            else:
                if text[i] == "\n":
                    output += text[i]
                    next_uppercase = False
                else:
                    next_uppercase = True

        return output

    def to_pascal_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_pascal_case_thread)

    def _to_pascal_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_pascal_case(self._text)
        task.return_value(outcome)

    def _to_pascal_case(self, text:str) -> str:

        output = ""
        next_uppercase = True

        for i in range(0, len(text)):
            if text[i].isalnum():
                if next_uppercase:
                    output += text[i].upper()
                    next_uppercase = False
                else:
                    output += text[i].lower()
            else:
                next_uppercase = True
                if text[i] == "\n":
                    output += text[i]

        return output

    def to_snake_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_snake_case_thread)

    def _to_snake_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_snake_case(self._text)
        task.return_value(outcome)

    def _to_snake_case(self, text:str) -> str:
        return self._snake_constant_kebab_cobol_converter(text, "_", False)

    def to_constant_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_constant_case_thread)

    def _to_constant_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_constant_case(self._text)
        task.return_value(outcome)

    def _to_constant_case(self, text:str) -> str:
        return self._snake_constant_kebab_cobol_converter(text, "_", True)

    def to_kebab_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_kebab_case_thread)

    def _to_kebab_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_kebab_case(self._text)
        task.return_value(outcome)

    def _to_kebab_case(self, text:str) -> str:
        return self._snake_constant_kebab_cobol_converter(text, "-", False)

    def to_cobol_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_cobol_case_thread)

    def _to_cobol_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_cobol_case(self._text)
        task.return_value(outcome)

    def _to_cobol_case(self, text:str) -> str:
        return self._snake_constant_kebab_cobol_converter(text, "-", True)

    def to_train_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_train_case_thread)

    def _to_train_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_train_case(self._text)
        task.return_value(outcome)

    def _to_train_case(self, text:str) -> str:

        ignore_next_non_alnum = True
        output = ""

        for i in range(0, len(text)):
            if text[i].isalnum():
                if ignore_next_non_alnum:
                    output += text[i].upper()
                else:
                    output += text[i].lower()
                ignore_next_non_alnum = False
            elif text[i] == "\n":
                ignore_next_non_alnum = True
                output += text[i]
            elif not ignore_next_non_alnum:
                if i < len(text)-1 and text[i+1].isalnum():
                    ignore_next_non_alnum = True
                    output += "-"

        return output

    def to_alternating_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_alternating_case_thread)

    def _to_alternating_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_alternating_case(self._text)
        task.return_value(outcome)

    def _to_alternating_case(self, text:str) -> str:
        return self._alternated_case(text, True)

    def to_reverse_alternating_case_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._to_reverse_alternating_case_thread)

    def _to_reverse_alternating_case_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._to_reverse_alternating_case(self._text)
        task.return_value(outcome)

    def _to_reverse_alternating_case(self, text:str) -> str:
        return self._alternated_case(text, False)

    def _alternated_case(self, text:str, start_with_lower:bool):
        output = ""

        for i in range(0, len(text)):
            if start_with_lower:
                output += text[i].lower()
            else:
                output += text[i].upper()

            start_with_lower = not start_with_lower

        return output

    def _snake_constant_kebab_cobol_converter(self, text:str, space_replacement:str, upper_case:bool):
        ignore_next_non_alnum = True
        output = ""

        for i in range(0, len(text)):
            if text[i].isalnum():
                ignore_next_non_alnum = False
                if upper_case:
                    output += text[i].upper()
                else:
                    output += text[i].lower()
            elif text[i] == "\n":
                ignore_next_non_alnum = True
                output += text[i]
            elif not ignore_next_non_alnum:
                if i < len(text)-1 and text[i+1].isalnum():
                    ignore_next_non_alnum = True
                    output += space_replacement

        return output
