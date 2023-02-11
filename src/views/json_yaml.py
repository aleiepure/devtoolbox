# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio
from gettext import gettext as _

from ..services.json_yaml import JsonYamlService
from ..utils import Utils


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/json_yaml.ui")
class JsonYamlView(Adw.Bin):
    __gtype_name__ = "JsonYamlView"

    # Template Elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _direction_selector = Gtk.Template.Child()
    _indents_spinner = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    # Service
    _service = JsonYamlService()

    def __init__(self):
        super().__init__()

        # Language highlight
        self._input_area.set_text_language_highlight("json")
        self._output_area.set_text_language_highlight("yaml")

        # Signals
        self._direction_selector.connect("toggled", self._on_direction_toggled)
        self._indents_spinner.connect("value-changed", self._on_input_changed)
        self._input_area.connect("text-changed", self._on_input_changed)
        self._input_area.connect("error", self._on_error)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._output_area.connect("error", self._on_error)

    def _on_direction_toggled(self, source_widget:GObject.Object):
        if self._direction_selector.get_left_btn_active() == True:
            self._input_area.set_text_language_highlight("json")
            self._output_area.set_text_language_highlight("yaml")
        else:
            self._input_area.set_text_language_highlight("yaml")
            self._output_area.set_text_language_highlight("json")
        self._convert()

    def _on_error(self, source_widget:GObject.Object, error:str):
        error_str = _("Error")
        self._toast.add_toast(Adw.Toast(title=f"{error_str}: {error}", priority=Adw.ToastPriority.HIGH))

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._service.get_cancellable().cancel()
        self._output_area.clear()

    def _on_input_changed(self, source_widget:GObject.Object):
        self._convert()

    def _convert(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        direction = self._direction_selector.get_left_btn_active()  # True: Json to yaml, False: Yaml to Json
        indents = int(self._indents_spinner.get_value())
        text = self._input_area.get_text()
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

    def _on_convert_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.convert_async_finish(result, self)
        self._output_area.set_text(outcome)
