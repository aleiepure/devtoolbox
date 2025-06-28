
# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio

from ..services.uuid_generator import UuidGeneratorService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/uuid_generator.ui")
class UuidGeneratorView(Adw.Bin):
    __gtype_name__ = "UuidGeneratorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _version_dropdown = Gtk.Template.Child()
    _amount_spinner = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    _service = UuidGeneratorService()

    def __init__(self):
        super().__init__()

        self._generate()

        # Signals
        self._version_dropdown.connect("notify::selected", self._on_version_changed)
        self._amount_spinner.connect("notify::value", self._on_amount_changed)

    def _on_version_changed(self, pspec:GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate()

    def _on_amount_changed(self, pspec:GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate()

    def _generate(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)

        # Setup task
        self._output_area.set_spinner_spin(True)
        self._service.set_version(self._version_dropdown.get_selected())
        self._service.set_amount(int(self._amount_spinner.get_value()))

        # Call task
        self._service.generate_async(self, self._on_generation_done)

    def _on_generation_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome = self._service.async_finish(result, self)

        if len(outcome) > 0:
            self._output_area.set_text(outcome)

        self._output_area.set_spinner_spin(False)
