# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio

from ..services.cron_converter import CronConverterService
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

    # Service
    _service = CronConverterService()

    def __init__(self):
        super().__init__()

        self._generate_dates()

        # Signals
        self._dates_spinner.connect("notify::value", self._on_dates_value_changed)
        self._format_text.connect("changed", self._on_format_changed)
        self._expression.connect("changed", self._on_expression_changed)
        self._expression.connect("cleared", self._on_expression_cleared)

    def _on_dates_value_changed(self, pspec: GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate_dates()

    def _on_format_changed(self, source_widget:GObject.Object):
        self._generate_dates()

    def _on_expression_changed(self, user_data:GObject.GPointer):
        self._generate_dates()

    def _on_expression_cleared(self, source_widget:GObject.Object):
        self._output_area.clear()

    def _generate_dates(self):
        self._expression.remove_css_class("border-red")

        expression = self._expression.get_text()
        format_str = self._format_text.get_text()
        number = int(self._dates_spinner.get_value())

        # Setup task
        self._service.set_expression(expression)
        self._service.set_format_str(format_str)
        self._service.set_quantity(number)

        if Utils.is_cron_expression_valid(expression):
            self._output_area.set_spinner_spin(True)
            self._service.generate_dates_async(self, self._on_generate_done)

        else:
            self._output_area.set_spinner_spin(False)
            if len(expression) != 0:
                self._expression.add_css_class("border-red")

    def _on_generate_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.generate_dates_async_finish(result, self)
        self._output_area.set_text(outcome)
