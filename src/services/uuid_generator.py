# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from uuid6 import uuid6, uuid7
import uuid
import random, string


class UuidGeneratorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_version(self, version:int):
        self._version = version

    def set_amount(self, amount:int):
        self._amount = amount

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._version = None
        self._amount = None
        return result.propagate_value().value

    def generate_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._generate_thread)

    def _generate_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._generate(self._version, self._amount)
        task.return_value(outcome)

    def _generate(self, version:int, amount:int) -> str:
        output = ""

        for _ in range(0, amount-1):
            match version:
                case 0: # Version-1
                    output += str(uuid.uuid1()) + "\n"
                case 1: # Version-3
                    output += str(uuid.uuid3(uuid.NAMESPACE_DNS, self._random_string())) + "\n"
                case 2: # Version-4
                    output += str(uuid.uuid4()) + "\n"
                case 3: # Version-5
                    output += str(uuid.uuid5(uuid.NAMESPACE_DNS, self._random_string())) + "\n"
                case 4: # Version-6
                    output += str(uuid6()) + "\n"
                case 5: # Version-7
                    output += str(uuid7()) + "\n"

        return output

    def _random_string(self) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(6))
