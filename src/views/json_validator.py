# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GObject
from gettext import gettext as _

from ..utils import Utils
from ..services.json_validator import JsonValidatorService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/json_validator.ui")
class JsonValidatorView(Adw.Bin):
    __gtype_name__ = "JsonValidatorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _json_textarea = Gtk.Template.Child()
    _schema_textarea = Gtk.Template.Child()
    _check_box = Gtk.Template.Child()
    _check_icon = Gtk.Template.Child()
    _check_title_lbl = Gtk.Template.Child()
    _check_lbl = Gtk.Template.Child()

    _service = JsonValidatorService()

    def __init__(self):
        super().__init__()

        self._json_textarea.set_text_language_highlight("json")
        self._schema_textarea.set_text_language_highlight("json")

        # Signals
        self._json_textarea.connect("text-changed", self._on_input_changed)
        self._schema_textarea.connect("text-changed", self._on_input_changed)
        self._json_textarea.connect("view-cleared", self._on_view_cleared)
        self._schema_textarea.connect("view-cleared", self._on_view_cleared)

    def _on_input_changed(self, source_widget:GObject.Object):
        self._check()

    def _on_view_cleared(self, source_widget:GObject.Object):
        if source_widget == self._json_textarea and len(self._schema_textarea.get_text()) == 0:
            self._check_box.set_visible(False)
        if source_widget == self._schema_textarea and len(self._json_textarea.get_text()) == 0:
            self._check_box.set_visible(False)
        self._service.get_cancellable().cancel()

    def _check(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._schema_textarea.remove_css_class("border-red")
        self._json_textarea.remove_css_class("border-red")

        # Setup task
        json = self._json_textarea.get_text()
        schema = self._schema_textarea.get_text()
        self._service.set_json(json)
        self._service.set_schema(schema)

        # Call task
        if len(json) > 0 and len(schema) > 0 and Utils.is_json(json) and Utils.is_json_schema(schema):
            self._service.check_json_async(self, self._on_check_done)

        if len(schema) > 0 and not Utils.is_json_schema(schema):
            self._schema_textarea.add_css_class("border-red")
        if len(json) > 0 and not Utils.is_json(json):
            self._json_textarea.add_css_class("border-red")

    def _on_check_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome, validation_error, schema_error = self._service.async_finish(result, self)
        if outcome:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("check-round-outline")
            self._check_title_lbl.set_text(_("Valid!"))
            self._check_lbl.set_wrap(False)
            self._check_lbl.set_text(_("JSON is compliant with the provided JSON schema."))
            self._check_icon.remove_css_class("error")
            self._check_title_lbl.remove_css_class("error")
            self._check_icon.add_css_class("success")
            self._check_title_lbl.add_css_class("success")
        elif validation_error:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("error")
            self._check_title_lbl.set_text(_("Invalid!"))
            self._check_lbl.set_wrap(True)
            self._check_lbl.set_text(_('JSON is not compliant with the provided JSON scheme:\n{validation_error}').format(validation_error=validation_error))
            self._check_icon.remove_css_class("success")
            self._check_title_lbl.remove_css_class("success")
            self._check_icon.add_css_class("error")
            self._check_title_lbl.add_css_class("error")
        elif schema_error:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("error")
            self._check_title_lbl.set_text(_("Invalid!"))
            self._check_lbl.set_wrap(True)
            self._check_lbl.set_text(_('Error in JSON schema:\n{schema_error}').format(schema_error=schema_error))
            self._check_icon.remove_css_class("success")
            self._check_title_lbl.remove_css_class("success")
            self._check_icon.add_css_class("error")
            self._check_title_lbl.add_css_class("error")
