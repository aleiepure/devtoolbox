# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gettext import gettext as _
from gi.repository import Gtk, Adw, GObject, Gio

from ..formatters.formatter import Formatter


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/formatter.ui")
class FormatterView(Adw.Bin):
    __gtype_name__ = "FormatterView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _tool_options = Gtk.Template.Child()
    _indents_spinner = Gtk.Template.Child()
    _textarea = Gtk.Template.Child()

    def __init__(self, formatter:Formatter):
        super().__init__()

        # Setup
        self._formatter = formatter
        self._title.set_property("title", formatter.get_title())
        self._title.set_property("description", formatter.get_description())
        self._title.set_property("tool-name", formatter.get_utility_name())
        self._tool_options.set_property("visible", formatter.get_show_options())
        self._textarea.set_property("name", formatter.get_textarea_name())
        self._textarea.set_property("text-language-highlight", formatter.get_language())
        self._textarea.set_property("custom-file-extensions", formatter.get_file_extensions())
        self._textarea.set_text_language_highlight(formatter.get_language())
        self._textarea.set_property("action-btn-name", formatter.get_action_button_name())

        # Signals
        self._indents_spinner.connect("notify::value", self._on_indents_changed)
        self._textarea.connect("action-clicked", self._on_format_clicked)
        self._textarea.connect("error", self._on_error)
        self._textarea.connect("view-cleared", self._on_view_cleared)

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._formatter.get_cancellable().cancel()
        self._textarea.set_spinner_spin(False)

    def _on_error(self, source_widget:GObject.Object, error:str):
        self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(error=error), priority=Adw.ToastPriority.HIGH))

    def _on_indents_changed(self, pspec: GObject.ParamSpec, user_data:GObject.GPointer):
        self._format_text()

    def _on_format_clicked(self, source_widget:GObject.Object):
        self._format_text()

    def _format_text(self):

        # Stop previous tasks
        self._formatter.get_cancellable().cancel()
        self._textarea.set_spinner_spin(False)
        self._textarea.remove_css_class("border-red")

        # Setup task
        self._textarea.set_spinner_spin(True)
        text = self._textarea.get_text()
        indents = int(self._indents_spinner.get_value())
        self._formatter.set_input(text)
        self._formatter.set_indentations(indents)

        # Call task
        if len(text) > 0 and self._formatter.is_correct(text):
            self._formatter.format_async(self, self._on_format_done)
        elif len(text) > 0:
            self._textarea.set_spinner_spin(False)
            self._textarea.add_css_class("border-red")
            self._toast.add_toast(Adw.Toast(title=_("Text is not in the correct format. Check if you misspelled something or if all parentheses are closed."), priority=Adw.ToastPriority.HIGH))
        else:
            self._textarea.set_spinner_spin(False)

    def _on_format_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(False)
        outcome = self._formatter.format_async_finish(result, self)
        self._textarea.set_text(outcome)
