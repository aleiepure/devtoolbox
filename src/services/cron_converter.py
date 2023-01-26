# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from crontab import CronTab, CronSlices


class CronConverterService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _generate_dates_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._generate_dates(self._expression, self._format_str, self._quantity)
        task.return_value(outcome)


    def _generate_dates(self, expression:str, format_str:str, quantity:int) -> str:
        cron = CronTab()
        job = cron.new(command="/usr/bin/echo")
        job.setall(expression)
        schedule = job.schedule()
        string = ""
        for _ in range(0, quantity):
            string += schedule.get_next().strftime(format_str) + "\n"
        return string

    def generate_dates_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._generate_dates_thread)

    def generate_dates_async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_expression(self, expression: str):
        self._expression = expression

    def set_format_str(self, format_str: str):
        self._format_str = format_str

    def set_quantity(self, quantity: int):
        self._quantity = quantity
