# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw
from gettext import gettext as _
from ..services.json_yaml import JsonYamlService
from ..utils import Utils


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/json_yaml.ui')
class JsonYamlView(Adw.Bin):
    __gtype_name__ = "JsonYamlView"

    # Template Elements
    _toast              = Gtk.Template.Child()
    _title              = Gtk.Template.Child()
    _direction_selector = Gtk.Template.Child()
    _indents_spinner    = Gtk.Template.Child()
    _input_area         = Gtk.Template.Child()
    _output_area        = Gtk.Template.Child()

    # Service
    _service = JsonYamlService()

    def __init__(self):
        super().__init__()

        # Signals
        self._direction_selector.connect("toggled", self._convert)
        self._indents_spinner.connect("value-changed", self._convert)
        self._input_area.connect("text-changed", self._convert)
        self._input_area.connect("error", self._on_error)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._output_area.connect("error", self._on_error)

    def _on_error(self, data, error):
        error_str = _("Error")
        self._toast.add_toast(Adw.Toast(title=f"{error_str}: {error}", priority=Adw.ToastPriority.HIGH))

    def _on_view_cleared(self, data):
        self._service.get_cancellable().cancel()
        self._output_area.clear()

    def _convert(self, data):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        direction = self._direction_selector.get_left_active() # True: Json to yaml, False: Yaml to Json
        indents   = int(self._indents_spinner.get_value())
        text      = self._input_area.get_text()
        self._service.set_input_string(text)
        self._service.set_input_indents(indents)
        if direction:
            if len(text) > 0 and Utils.is_json(text):
                self._output_area.set_spinner_spin(True)
                self._service.convert_json_to_yaml_async(self, self._on_convert_done)
            else:
                self._output_area.set_spinner_spin(False)
                self._input_area.add_css_class("border-red")
        else:
            if len(text) > 0 and Utils.is_yaml(text):
                self._output_area.set_spinner_spin(True)
                self._service.convert_yaml_to_json_async(self, self._on_convert_done)
            else:
                self._output_area.set_spinner_spin(False)
                self._input_area.add_css_class("border-red")

    def _on_convert_done(self, source_object, result, data):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.convert_async_finish(result, self)
        self._output_area.set_text(outcome)
