# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, GObject
from gettext import gettext as _

from ..services.lorem_generator import LoremGeneratorService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/lorem_generator.ui")
class LoremGeneratorView(Adw.Bin):
    __gtype_name__ = "LoremGeneratorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _begin_with_switch = Gtk.Template.Child()
    _quantity_combo = Gtk.Template.Child()
    _quantity_spinner = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    _service = LoremGeneratorService()

    def __init__(self):
        super().__init__()

        self._generate_text()

        # Signals
        self._begin_with_switch.connect("notify::active", self._on_begin_with_switch_changed)
        self._quantity_combo.connect("notify::selected", self._on_quantity_combo_changed)
        self._quantity_spinner.connect("value-changed", self._on_quantity_spinner_changed)

    def _on_begin_with_switch_changed(self, pspec:GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate_text()

    def _on_quantity_combo_changed(self, pspec:GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate_text()

    def _on_quantity_spinner_changed(self, user_data:GObject.GPointer):
        self._generate_text()

    def _generate_text(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)

        # Setup task
        self._output_area.set_spinner_spin(True)
        self._service.set_beginning(self._begin_with_switch.get_active())
        self._service.set_amount(self._quantity_combo.get_selected(), int(self._quantity_spinner.get_value()))

        # Call task
        self._service.generate_text_async(self, self._on_generate_done)

    def _on_generate_done(self, source_object, result, data):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.async_finish(result, self)
        self._output_area.set_text(outcome)
