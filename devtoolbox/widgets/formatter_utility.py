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
from gi.repository import Gtk, Adw, Gio, Gdk


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/formatter_utility.ui")
class FormatterUtility(Adw.Bin):
    __gtype_name__ = "FormatterUtility"

    title = Gtk.Template.Child()
    subtitle = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    toast = Gtk.Template.Child()
    indents_spinner = Gtk.Template.Child()
    format_btn = Gtk.Template.Child()
    open_btn = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    input_textview = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, formatter):
        super().__init__()

        self.formatter = formatter

        # Set titles
        self.title.set_label(self.title.get_label().replace(
            "Placeholder", self.formatter.get_name()))
        self.subtitle.set_label(self.subtitle.get_label().replace(
            "Placeholder", self.formatter.get_name()))

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index(self.formatter.get_settings_name())
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Signals
        self.open_btn.connect("clicked", self.on_open_clicked)
        self.copy_btn.connect("clicked", self.on_copy_clicked)
        self.paste_btn.connect("clicked", self.on_paste_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.format_btn.connect("clicked", self.on_format_clicked)
        self.input_textview.get_buffer().connect("changed", self.on_text_changed)
    
    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index(self.formatter.get_settings_name())
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index(self.formatter.get_settings_name())
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove(self.formatter.get_settings_name())
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append(self.formatter.get_settings_name())
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_open_clicked(self, data):

        self._native = Gtk.FileChooserNative(
            title="Open File",
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel"
        )

        # File filter
        file_filter = Gtk.FileFilter()
        for s in self.formatter.get_file_extensions():
            file_filter.add_suffix(s)
        file_filter.set_name(self.formatter.get_name() + " Files")
        self._native.add_filter(file_filter)

        # Connect the "response" signal
        self._native.connect("response", self.on_open_response)
        self._native.show()

    def on_open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.open_file(dialog.get_file())

        # Delete filechooser
        self._native = None

    def open_file(self, file):
        file.load_contents_async(None, self.open_file_complete)

    def open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)

        # Check if file is valid
        if not contents[0]:
            path = file.peek_path()
            self.toast.add_toast(
                Adw.Toast(title=_(f"Error opening file {path}")))
            return

        # Determine if file is text
        if self.formatter.is_text(contents[1]):
            text = contents[1].decode("utf-8")
        else:
            path = file.peek_path()
            self.toast.add_toast(
                Adw.Toast(title=_(f"{path}: Not a supported json file")))
            return

        # Insert in textview
        buffer = self.input_textview.get_buffer()
        buffer.set_text(text)
        buffer.place_cursor(buffer.get_end_iter())

    def on_paste_clicked(self, data):
        buffer = self.input_textview.get_buffer()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        buffer.paste_clipboard(clipboard, None, True)

    def on_clear_clicked(self, data):
        buffer = self.input_textview.get_buffer()
        buffer.set_text("")

    def on_copy_clicked(self, data):
        buffer = self.input_textview.get_buffer()
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_text_changed(self, data):
        self.input_textview.remove_css_class("border-red")

    def on_format_clicked(self, data):

        buffer = self.input_textview.get_buffer()
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        indents = int(self.indents_spinner.get_value())

        result, formated_text = self.formatter.indent(text, indents)
        if result:
            buffer.set_text(formated_text)
        else:
            self.input_textview.add_css_class("border-red")
            self.toast.add_toast(
                Adw.Toast(title=_("Text cannot be formatted: invalid " + self.formatter.get_name() + " syntax")))