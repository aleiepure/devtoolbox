# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, GObject, Gio
from gettext import gettext as _
import base64
import json
import urllib.parse as urlparse
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
    _signature_selector = Gtk.Template.Child()
    _key_encoding_selector = Gtk.Template.Child()
    _key_encoding_selector_row = Gtk.Template.Child()
    _key_row = Gtk.Template.Child()
    _asymmetric_box = Gtk.Template.Child()
    _public_key_area = Gtk.Template.Child()
    _private_key_area = Gtk.Template.Child()
    _check_box = Gtk.Template.Child()
    _check_icon = Gtk.Template.Child()
    _check_title_lbl = Gtk.Template.Child()
    _check_lbl = Gtk.Template.Child()

    _invalid_toast = Adw.Toast(title=_("Invalid value. Please check again"))

    _service = JwtDecoderService()

    def __init__(self):
        super().__init__()

        # Fix layout
        self._token_area.get_child().set_size_request(-1, 160)
        self._token_area.get_child().set_vexpand(False)
        self._token_area.get_child().set_vexpand_set(True)
        self._asymmetric_box.set_size_request(-1, 160)
        self._asymmetric_box.set_vexpand(False)
        self._asymmetric_box.set_vexpand_set(True)

        # Signals
        self._token_area.connect("view-cleared", self._on_view_cleared)
        self._token_area_handler = self._token_area.connect("text-changed", self._on_token_changed)
        self._header_area_handler = self._header_area.connect("text-changed", self._on_header_payload_changed)
        self._payload_area_handler = self._payload_area.connect("text-changed", self._on_header_payload_changed)
        self._signature_selector.connect("notify::active-name", self._on_signature_selector)
        self._key_encoding_selector.connect("notify::active-name", self._on_key_row_changed)
        self._key_row.connect("notify::text", self._on_key_row_changed)

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._header_area.clear()
        self._payload_area.clear()

    def _on_token_changed(self, source_widget:GObject.Object):
        self._reset_areas()

        # Setup task
        token = self._token_area.get_text()
        self._service.set_token(token)
        if len(token) > 0 and Utils.is_jwt_token(token):
            self._header_area.set_spinner_spin(True)
            self._payload_area.set_spinner_spin(True)
            self._service.decode_header_async(self, self._on_header_decode_done)
            self._service.decode_payload_async(self, self._on_payload_decode_done)
            if self._is_signature():
                self._service.set_public_key(self._get_public_key())
                self._service.verify_signature_async(self, self._on_verify_signature_done)
        elif len(token) > 0:
            self._header_area.set_spinner_spin(False)
            self._payload_area.set_spinner_spin(False)
            self._token_area.add_css_class("border-red")
            self._toast.add_toast(self._invalid_toast)
        else:
            self._on_view_cleared(self._token_area)

    def _on_header_payload_changed(self, source_widget:GObject.Object):
        self._reset_areas()

        # Setup task
        header = self._header_area.get_text()
        payload = self._payload_area.get_text()
        key = self._get_private_key() if self._is_signature() else None

        if source_widget == self._payload_area and header.strip() == "":
            match self._signature_selector.get_active_name():
                case "symmetric":
                    default_alg = "HS256"
                case "asymmetric":
                    default_alg = "RS256"
                case _:
                    default_alg = "none"
            header = json.dumps({"alg": default_alg, "typ": "JWT"}, indent=4)
            self._header_area.handler_block(self._header_area_handler)
            self._header_area.set_text(header)
            self._header_area.handler_unblock(self._header_area_handler)
        elif source_widget == self._payload_area and payload.strip() == "":
            payload = json.dumps({}, indent=4)
            self._payload_area.handler_block(self._payload_area_handler)
            self._payload_area.set_text(payload)
            self._payload_area.handler_unblock(self._payload_area_handler)

        if Utils.is_json(header) and Utils.is_json(payload):
            self._service.set_header(header)
            self._service.set_payload(payload)
            self._service.set_private_key(key)
            self._token_area.set_spinner_spin(True)
            self._service.encode_token_async(self, self._on_token_encode_done)
        else:
            if not Utils.is_json(header):
                self._header_area.add_css_class("border-red")
                self._toast.add_toast(self._invalid_toast)
            if not Utils.is_json(payload):
                self._payload_area.add_css_class("border-red")
                self._toast.add_toast(self._invalid_toast)

    def _on_signature_selector(self, *__):
        is_symmetric = self._signature_selector.get_active_name() == "symmetric"
        is_asymmetric = self._signature_selector.get_active_name() == "asymmetric"
        if self._signature_selector.get_active_name() == "off":
            self._check_box.set_visible(False)
        self._key_encoding_selector_row.set_visible(is_symmetric)
        self._key_row.set_visible(is_symmetric)
        self._asymmetric_box.set_visible(is_asymmetric)
        self._on_token_changed(self._token_area)

    def _on_key_row_changed(self, *__):
        if (self._key_encoding_selector.get_active_name() == "base64url"
                and not Utils.is_base64url(urlparse.unquote(self._key_row.get_text()) + "==")):
            self._key_row.add_css_class("border-red")
            self._toast.add_toast(self._invalid_toast)
            return
        self._key_row.remove_css_class("border-red")
        self._on_token_changed(self._token_area)

    def _on_header_decode_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome = self._service.task_finish(result, self)
        self._header_area.set_spinner_spin(False)
        self._header_area.handler_block(self._header_area_handler)
        if outcome is not None:
            self._header_area.set_text(outcome)
        else:
            self._header_area.set_text("")
            self._token_area.add_css_class("border-red")
            self._toast.add_toast(self._invalid_toast)
        self._header_area.handler_unblock(self._header_area_handler)

    def _on_payload_decode_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome = self._service.task_finish(result, self)
        self._payload_area.set_spinner_spin(False)
        self._payload_area.handler_block(self._payload_area_handler)
        if outcome is not None:
            self._payload_area.set_text(outcome)
        else:
            self._header_area.set_text("")
            self._token_area.add_css_class("border-red")
            self._toast.add_toast(self._invalid_toast)
        self._payload_area.handler_unblock(self._payload_area_handler)

    def _on_verify_signature_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome = self._service.task_finish(result, self)
        if outcome:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("check-round-outline")
            self._check_title_lbl.set_text(_("Signature is Valid!"))
            self._check_lbl.set_wrap(False)
            self._check_lbl.set_text(_("The JWT signature was verified successfully."))
            self._check_icon.remove_css_class("warning")
            self._check_title_lbl.remove_css_class("warning")
            self._check_icon.add_css_class("success")
            self._check_title_lbl.add_css_class("success")
        else:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("warning")
            self._check_title_lbl.set_text(_("Warning, Signature is Invalid!"))
            self._check_lbl.set_wrap(True)
            self._check_lbl.set_text(
                _("The JWT signature doesn't match the provided key. "
                  "Please verify the key encoding or ensure the token was signed correctly."))
            self._check_icon.remove_css_class("success")
            self._check_title_lbl.remove_css_class("success")
            self._check_icon.add_css_class("warning")
            self._check_title_lbl.add_css_class("warning")

    def _on_token_encode_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome = self._service.task_finish(result, self)
        self._token_area.set_spinner_spin(False)
        self._token_area.handler_block(self._token_area_handler)
        if outcome is not None:
            self._token_area.set_text(outcome)
        else:
            self._token_area.set_text("")
            self._header_area.add_css_class("border-red")
            self._payload_area.add_css_class("border-red")
            self._toast.add_toast(self._invalid_toast)
        self._token_area.handler_unblock(self._token_area_handler)

    def _reset_areas(self):
        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._check_box.set_visible(False)
        self._token_area.set_spinner_spin(False)
        self._header_area.set_spinner_spin(False)
        self._payload_area.set_spinner_spin(False)
        self._token_area.remove_css_class("border-red")
        self._header_area.remove_css_class("border-red")
        self._payload_area.remove_css_class("border-red")

    def _is_signature(self) -> bool:
        return self._signature_selector.get_active_name() in ("symmetric", "asymmetric")

    def _get_symmetric_key(self) -> str | bytes:
        key_text = self._key_row.get_text()
        if self._key_encoding_selector.get_active_name() == "base64url":
            return base64.urlsafe_b64decode(urlparse.unquote(key_text) + "==")
        else:
            return key_text

    def _get_public_key(self) -> str | bytes:
        if self._signature_selector.get_active_name() == "symmetric":
            return self._get_symmetric_key()
        else:
            return self._public_key_area.get_text()

    def _get_private_key(self) -> str | bytes:
        if self._signature_selector.get_active_name() == "symmetric":
            return self._get_symmetric_key()
        else:
            return self._private_key_area.get_text()

