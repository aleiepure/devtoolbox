# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gdk
from crontab import CronTab, CronSlices
from ..utils import Utils


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/cron_converter.ui")
class CronConverterView(Adw.Bin):
    __gtype_name__ = "CronConverterView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _dates_spinner = Gtk.Template.Child()
    _format_text = Gtk.Template.Child()
    _expression = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._generate_dates()

        # Signals
        self._dates_spinner.connect("value-changed", self._on_dates_value_changed)
        self._format_text.connect("changed", self._on_format_changed)
        self._expression.connect("changed", self._on_expression_changed)
        self._expression.connect("cleared", self._on_expression_cleared)

    def _on_dates_value_changed(self, widget):
        self._generate_dates()

    def _on_format_changed(self, widget):
        self._generate_dates()

    def _on_expression_changed(self, widget):
        self._generate_dates()

    def _on_expression_cleared(self, widget):
        self._output_area.clear()

    def _generate_dates(self):
        self._expression.remove_css_class("border-red")

        expression = self._expression.get_text()
        format_str = self._format_text.get_text()
        number = int(self._dates_spinner.get_value())

        if Utils.is_cron_expression_valid(expression):
            cron = CronTab()
            job = cron.new(command="/usr/bin/echo")
            job.setall(expression)
            schedule = job.schedule()
            string = ""
            for _ in range(0, number):
                string += schedule.get_next().strftime(format_str) + "\n"
            self._output_area.set_text(string)
        else:
            if len(expression) != 0:
                self._expression.add_css_class("border-red")