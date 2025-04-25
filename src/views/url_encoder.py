# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio
from gettext import gettext as _

from ..services.url_encoder import UrlEncoderService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/url_encoder.ui")
class UrlEncoderView(Adw.Bin):
    __gtype_name__ = "UrlEncoderView"

    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _preference_group = Gtk.Template.Child()
    _direction_selector = Gtk.Template.Child()
    _space_encoding_row = Gtk.Template.Child()
    _space_encoding_selector = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    _service = UrlEncoderService()

    def __init__(self):
        super().__init__()

        # Signals
        # self._direction_selector.connect("toggled", self._on_input_changed)
        # self._space_encoding_selector.connect(
            # "toggled", self._on_input_changed)
        self._input_area.connect("text-changed", self._on_input_changed)
        self._input_area.connect("error", self._on_error)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._output_area.connect("error", self._on_error)

    @Gtk.Template.Callback()
    def _on_direction_changed(self,
                              pspec: GObject.GParamSpec,
                              user_data: GObject.GPointer = None) -> None:
        self._space_encoding_row.set_visible(
            self._direction_selector.get_active() == 0)
        self._convert()
        
    @Gtk.Template.Callback()
    def _on_space_encoding_changed(self,
                                      pspec: GObject.GParamSpec,
                                      user_data: GObject.GPointer = None) -> None:
          self._convert()

    def _on_input_changed(self, source_widget: GObject.Object):
        if self._direction_selector.get_active() == 0:
            self._space_encoding_row.set_visible(True)
        else:
            self._space_encoding_row.set_visible(False)
        self._convert()

    def _on_view_cleared(self, source_widget: GObject.Object):
        self._output_area.clear()

    def _on_error(self, source_widget: GObject.Object, error: str):
        self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(
            error=error), priority=Adw.ToastPriority.HIGH))

    def _convert(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        text = self._input_area.get_text()
        space = self._space_encoding_selector.get_active() == 0  # True: +, False: %20
        self._service.set_input(text)
        self._service.set_space_as_plus(space)

        # Call task
        if self._direction_selector.get_active() == 0:  # True: encode, False: decode
            self._output_area.set_spinner_spin(True)
            self._service.encode_async(self, self._on_async_done)
        else:
            self._output_area.set_spinner_spin(True)
            self._service.decode_async(self, self._on_async_done)

    def _on_async_done(self, source_widget: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.async_finish(result, self)
        self._output_area.set_text(outcome)
