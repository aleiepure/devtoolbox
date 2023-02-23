# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject, Gio
import lorem


class LoremGeneratorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def async_finish(self, result:Gio.AsyncResult, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._begin_with_lorem_ipsum = None
        self._unit = None
        self._quantity = None
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_beginning(self, begin_with_lorem_ipsum:bool):
        self._begin_with_lorem_ipsum = begin_with_lorem_ipsum

    def set_amount(self, unit:int, quantity:int):
        self._unit = unit
        self._quantity = quantity

    def generate_text_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._generate_text_thread)

    def _generate_text_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._generate_text(self._begin_with_lorem_ipsum, self._unit, self._quantity)
        task.return_value(outcome)

    def _generate_text(self, begin_with_lorem_ipsum:bool, unit:int, quantity:int) -> str:
        string = ""

        match unit:
            case 0: # words
                string = lorem.get_word(count=quantity)
            case 1: # sentence
                string = lorem.get_sentence(count=quantity)
            case 2: # paragraph
                string = lorem.get_paragraph(count=quantity)

        if begin_with_lorem_ipsum:
            string = "Lorem ipsum dolor sit amet, " + string[0].lower() + string[1:]

        return string
