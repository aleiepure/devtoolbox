# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gdk, GObject, Gio, GLib, GtkSource
from gettext import gettext as _

from ..utils import Utils
from ..services.regex_tester import RegexTesterService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/regex_tester.ui")
class RegexTesterView(Adw.Bin):
    __gtype_name__ = "RegexTesterView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _regex_entry = Gtk.Template.Child()
    _textarea = Gtk.Template.Child()

    _service = RegexTesterService()

    def __init__(self):
        super().__init__()

        # Signals
        self._regex_entry.connect("changed", self._on_regex_changed)
        self._textarea.connect("text-changed", self._on_text_changed)
        self._regex_entry.connect("cleared", self._on_regex_cleared)

    def _on_regex_cleared(self, source_widget:GObject.Object):
        buffer = self._textarea.get_buffer()
        self._textarea.set_spinner_spin(False)
        self._regex_entry.remove_css_class("border-red")
        buffer.remove_all_tags(buffer.get_start_iter(), buffer.get_end_iter())
        self._service.get_cancellable().cancel()

    def _on_regex_changed(self, user_data:GObject.GPointer):
        self._search()

    def _on_text_changed(self, user_data:GObject.GPointer):
        self._search()

    def _search(self):

        # Stop previous tasks
        buffer = self._textarea.get_buffer()
        self._service.get_cancellable().cancel()
        self._textarea.set_spinner_spin(False)
        self._regex_entry.remove_css_class("border-red")
        buffer.remove_all_tags(buffer.get_start_iter(), buffer.get_end_iter())

        # Setup task
        self._textarea.set_spinner_spin(True)
        self._service.set_regex(self._regex_entry.get_text())
        self._service.set_buffer(buffer)

        # Call task
        if len(self._regex_entry.get_text()) > 0 and Utils.is_regex(self._regex_entry.get_text()):
            self._service.find_all_matches_async(self, self._on_find_done)
        elif len(self._regex_entry.get_text()) > 0:
            self._regex_entry.add_css_class("border-red")
            self._textarea.set_spinner_spin(False)
        else:
            self._textarea.set_spinner_spin(False)

    def _on_find_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome = self._service.async_finish(result, self)
        self._textarea.set_spinner_spin(False)
