# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GObject
from gettext import gettext as _

from ..utils import Utils
from ..services.xml_validator import XmlValidatorService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/xml_validator.ui")
class XmlValidatorView(Adw.Bin):
    __gtype_name__ = "XmlValidatorView"

    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _xml_textarea = Gtk.Template.Child()
    _xsd_textarea = Gtk.Template.Child()
    _check_box = Gtk.Template.Child()
    _check_icon = Gtk.Template.Child()
    _check_title_lbl = Gtk.Template.Child()
    _check_lbl = Gtk.Template.Child()

    _service = XmlValidatorService()

    def __init__(self):
        super().__init__()

        self._xml_textarea.set_text_language_highlight("xml")
        self._xsd_textarea.set_text_language_highlight("xml")

        # Signals
        self._xml_textarea.connect("text-changed", self._on_input_changed)
        self._xsd_textarea.connect("text-changed", self._on_input_changed)
        self._xml_textarea.connect("view-cleared", self._on_view_cleared)
        self._xsd_textarea.connect("view-cleared", self._on_view_cleared)

    def _on_input_changed(self, source_widget:GObject.Object):
        self._check()

    def _on_view_cleared(self, source_widget:GObject.Object):
        if source_widget == self._xml_textarea and len(self._xsd_textarea.get_text()) == 0:
            self._check_box.set_visible(False)
        if source_widget == self._xsd_textarea and len(self._xml_textarea.get_text()) == 0:
            self._check_box.set_visible(False)
        self._service.get_cancellable().cancel()

    def _check(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._xsd_textarea.remove_css_class("border-red")
        self._xml_textarea.remove_css_class("border-red")

        # Setup task
        xml = self._xml_textarea.get_text()
        xsd = self._xsd_textarea.get_text()
        self._service.set_xml(xml)
        self._service.set_xsd(xsd)

        # Call task
        if len(xml) > 0 and len(xsd) > 0 and Utils.is_xml(xml) and Utils.is_xsd(xsd):
            self._service.check_xml_async(self, self._on_check_done)

        if len(xsd) > 0 and not Utils.is_xsd(xsd):
            self._xsd_textarea.add_css_class("border-red")
        if len(xml) > 0 and not Utils.is_xml(xml):
            self._xml_textarea.add_css_class("border-red")

    def _on_check_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome, xsd_error, parsing_error = self._service.async_finish(result, self)
        if outcome:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("check-round-outline")
            self._check_title_lbl.set_text(_("Valid!"))
            self._check_lbl.set_wrap(False)
            self._check_lbl.set_text(_("XML is compliant with the provided XSD schema."))
            self._check_icon.remove_css_class("error")
            self._check_title_lbl.remove_css_class("error")
            self._check_icon.add_css_class("success")
            self._check_title_lbl.add_css_class("success")
        elif xsd_error:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("error")
            self._check_title_lbl.set_text(_("Invalid!"))
            self._check_lbl.set_wrap(True)
            self._check_lbl.set_text(_('XML is not compliant with the provided XSD scheme:\n{xsd_error}').format(xsd_error=xsd_error))
            self._check_icon.remove_css_class("success")
            self._check_title_lbl.remove_css_class("success")
            self._check_icon.add_css_class("error")
            self._check_title_lbl.add_css_class("error")
        elif parsing_error:
            self._xsd_textarea.add_css_class("border-red")
            self._toast.add_toast(Adw.Toast(title=parsing_error, priority=Adw.ToastPriority.HIGH))
