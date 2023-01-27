# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw
from gettext import gettext as _
from ..utils import Utils
from ..services.html_encoder import HtmlEncoderService

@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/html_encoder.ui")
class HtmlEncoderView(Adw.Bin):
    __gtype_name__ = "HtmlEncoderView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _direction_selector = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    _service = HtmlEncoderService()

    def __init__(self):
        super().__init__()

        # Language highlight
        self._input_area.set_text_language_highlight("html")
        self._output_area.set_text_language_highlight("html")

        # Signals
        self._direction_selector.connect("toggled", self._convert)
        self._input_area.connect("text-changed", self._convert)
        self._input_area.connect("error", self._on_error)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._output_area.connect("error", self._on_error)

    def _on_view_cleared(self, data):
        self._output_area.clear()

    def _on_error(self, data, error):
        error_str = _("Error")
        self._toast.add_toast(Adw.Toast(title=f"{error_str}: {error}", priority=Adw.ToastPriority.HIGH))

    def _convert(self, data):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        text = self._input_area.get_text()
        self._service.set_input(text)

        # Call task
        if self._direction_selector.get_left_active(): # True: encode, False: decode
            self._output_area.set_spinner_spin(True)
            self._service.encode_async(self, self._on_async_done)
        else:
            self._output_area.set_spinner_spin(True)
            self._service.decode_async(self, self._on_async_done)

    def _on_async_done(self, source_object, result, data):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.async_finish(result, self)
        self._output_area.set_text(outcome)
