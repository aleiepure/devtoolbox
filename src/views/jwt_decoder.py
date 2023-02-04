# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk
from ..utils import Utils
from ..services.jwt_decoder import JwtDecoderService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/jwt_decoder.ui")
class JwtDecoderView(Adw.Bin):
    __gtype_name__ = "JwtDecoderView"

    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _token_area = Gtk.Template.Child()
    _header_area = Gtk.Template.Child()
    _payload_area = Gtk.Template.Child()

    _service = JwtDecoderService()

    def __init__(self):
        super().__init__()

        self._token_area.connect("view-cleared", self._on_view_cleared)
        self._token_area.connect("text-changed", self._on_token_changed)

    def _on_view_cleared(self, data):
        self._header_area.clear()
        self._payload_area.clear()

    def _on_token_changed(self, data):
        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._header_area.set_spinner_spin(False)
        self._payload_area.set_spinner_spin(False)
        self._token_area.remove_css_class("border-red")

        # Setup task
        token = self._token_area.get_text()
        self._service.set_token(token)
        if len(token) > 0 and Utils.is_jwt_token(token):
            self._header_area.set_spinner_spin(True)
            self._payload_area.set_spinner_spin(True)
            self._service.decode_header_async(self, self._on_header_decode_done)
            self._service.decode_payload_async(self, self._on_payload_decode_done)
        elif len(token) > 0:
            self._header_area.set_spinner_spin(False)
            self._payload_area.set_spinner_spin(False)
            self._token_area.add_css_class("border-red")

    def _on_header_decode_done(self, source_object, result, data):
        outcome = self._service.decode_finish(result, self)
        self._header_area.set_spinner_spin(False)
        self._header_area.set_text(outcome)

    def _on_payload_decode_done(self, source_object, result, data):
        outcome = self._service.decode_finish(result, self)
        self._payload_area.set_spinner_spin(False)
        self._payload_area.set_text(outcome)
