# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GLib
from gettext import gettext as _

from ..services.json_yaml_toml import JsonYamlTomlService
from ..utils import Utils


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/json_yaml_toml.ui")
class JsonYamlTomlView(Adw.Bin):
    __gtype_name__ = "JsonYamlView"

    # Template Elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _input_format_selector = Gtk.Template.Child()
    _output_format_selector = Gtk.Template.Child()
    _indents_row = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    # Service
    _service = JsonYamlTomlService()

    def __init__(self):
        super().__init__()

        # Language highlight
        self._input_area.set_text_language_highlight("json")
        self._output_area.set_text_language_highlight("yaml")

        GLib.idle_add(self._initialize_format_state)
        
    def _initialize_format_state(self):
        self._input_format_selector.set_active(0)   # JSON
        self._output_format_selector.set_active(1)  # YAML
        return False

    @Gtk.Template.Callback()
    def _on_format_changed_signal(self, widget: Adw.ToggleGroup, pspec: GObject.ParamSpec):
        formats = ["json", "yaml", "toml"]

        input_selector = self.get_template_child(JsonYamlTomlView, "_input_format_selector")
        output_selector = self.get_template_child(JsonYamlTomlView, "_output_format_selector")

        # Validate indices
        input_active = input_selector.get_active()
        output_active = output_selector.get_active()
        if input_active < 0 or input_active >= len(formats) or output_active < 0 or output_active >= len(formats):
            return

        # Same format, auto-select a different one
        if input_active == output_active and widget == input_selector:
            for i in range(3):
                if i != input_active:
                    output_selector.set_active(i)
                    output_active = i
                    break

        input_format = formats[input_active]
        output_format = formats[output_active]

        # Update syntax highlighting
        self._input_area.set_text_language_highlight(input_format)
        self._output_area.set_text_language_highlight(output_format)

        self._convert()

    @Gtk.Template.Callback()
    def _on_error_signal(self, source_widget: GObject.Object, error: str):
        self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(
            error=error), priority=Adw.ToastPriority.HIGH))

    @Gtk.Template.Callback()
    def _on_view_cleared_signal(self, source_widget: GObject.Object):
        self._service.get_cancellable().cancel()
        self._output_area.clear()

    @Gtk.Template.Callback()
    def _on_input_changed_signal(self, source_widget: GObject.Object):
        self._convert()

    @Gtk.Template.Callback()
    def _is_format_enabled_closure(self, source: GObject.Object, active: int, index: int) -> bool:
        return active != index

    def _convert(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        input_selector = self.get_template_child(JsonYamlTomlView, "_input_format_selector")
        output_selector = self.get_template_child(JsonYamlTomlView, "_output_format_selector")
        input_format = input_selector.get_active()
        output_format = output_selector.get_active()

        # Validate formats
        # Safety check for valid indices
        if input_format < 0 or input_format > 2 or output_format < 0 or output_format > 2:
            return
        if input_format == output_format:
            return

        indents = int(self._indents_row.get_value())
        text = self._input_area.get_text()

        if len(text) == 0:
            return

        self._service.set_input_string(text)
        self._service.set_input_indents(indents)

        # Validate input and convert
        if input_format == 0:  # JSON
            if not Utils.is_json(text):
                self._input_area.add_css_class("border-red")
                return

            if output_format == 1:  # JSON → YAML
                self._output_area.set_spinner_spin(True)
                self._service.convert_json_to_yaml_async(
                    self, self._on_convert_done)

            elif output_format == 2:  # JSON → TOML
                self._output_area.set_spinner_spin(True)
                self._service.convert_json_to_toml_async(
                    self, self._on_convert_done)

        elif input_format == 1:  # YAML
            if not Utils.is_yaml(text):
                self._input_area.add_css_class("border-red")
                return

            if output_format == 0:  # YAML → JSON
                self._output_area.set_spinner_spin(True)
                self._service.convert_yaml_to_json_async(
                    self, self._on_convert_done)

            elif output_format == 2:  # YAML → TOML
                self._output_area.set_spinner_spin(True)
                self._service.convert_yaml_to_toml_async(
                    self, self._on_convert_done)

        elif input_format == 2:  # TOML
            if not Utils.is_toml(text):
                self._input_area.add_css_class("border-red")
                return

            if output_format == 0:  # TOML → JSON
                self._output_area.set_spinner_spin(True)
                self._service.convert_toml_to_json_async(
                    self, self._on_convert_done)

            elif output_format == 1:  # TOML → YAML
                self._output_area.set_spinner_spin(True)
                self._service.convert_toml_to_yaml_async(
                    self, self._on_convert_done)

    def _on_convert_done(self, source_widget: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.convert_async_finish(result, self)
        self._output_area.set_text(outcome)
