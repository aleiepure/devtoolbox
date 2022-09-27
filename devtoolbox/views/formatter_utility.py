# formatter_utility.py
#
# Copyright 2022 Alessandro Iepure
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gettext import gettext as _
from gi.repository import Gtk, Adw


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/formatter_utility.ui")
class FormatterUtility(Adw.Bin):
    __gtype_name__ = "FormatterUtility"

    toast = Gtk.Template.Child()
    titlebar = Gtk.Template.Child()
    indents_spinner = Gtk.Template.Child()
    textarea = Gtk.Template.Child()

    def __init__(self, formatter):
        super().__init__()

        self.formatter = formatter

        # Set syntax higlight
        self.textarea.set_text_language_highlight(self.formatter.get_name().lower())

        # Set titles
        self.titlebar.set_title(self.titlebar.get_title().replace(
            "Placeholder", self.formatter.get_name()))
        self.titlebar.set_description(self.titlebar.get_description().replace(
            "Placeholder", self.formatter.get_name()))
        self.titlebar.set_utility_name(self.titlebar.get_utility_name().replace("Placeholder", self.formatter.get_utility_name()))

        # File extensions
        self.textarea.custom_file_extensions = self.formatter.get_file_extensions()

        # Signals
        self.indents_spinner.connect("value-changed", self.on_indents_changed)
        self.textarea.connect("action-clicked", self.on_format_clicked)
        self.textarea.connect("text-changed", self.on_text_changed)
        self.textarea.connect("error", self.on_error)

    def on_error(self, error):
        self.toast.add_toast(
                Adw.Toast(title=f"Error: {error}"))
        
    def on_indents_changed(self, data):
        self._format()

    def on_text_changed(self, data):
       self.textarea.remove_css_class("border-red")

    def on_format_clicked(self, widget, data):
        self._format()

    def _format(self):
        text = self.textarea.get_text()
        indents = int(self.indents_spinner.get_value())

        result, formated_text = self.formatter.indent(text, indents)
        if result:
            self.textarea.get_buffer().set_text(formated_text)
        else:
            self.textarea.add_css_class("border-red")
            self.toast.add_toast(
                Adw.Toast(title=_("Text cannot be formatted: invalid " + self.formatter.get_name() + " syntax")))