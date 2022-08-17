# json2yaml_utility.py
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

from ..service.json2yaml import JSON2YAML
from gettext import gettext as _
from gi.repository import Gtk, Adw, Gdk, Gio


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/json2yaml_utility.ui")
class Json2YamlUtility(Adw.Bin):
    __gtype_name__ = "Json2YamlUtility"

    starred_btn = Gtk.Template.Child()
    open_btn = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()
    input_textview = Gtk.Template.Child()
    output_textview = Gtk.Template.Child()
    toast = Gtk.Template.Child()
    direction_toggle = Gtk.Template.Child()
    indents_spinner = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    # True: JSON to YAML, False: YAML to JSON
    direction = True

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("json2yaml")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Signals

        self.open_btn.connect("clicked", self.on_open_clicked)
        self.paste_btn.connect("clicked", self.on_paste_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.copy_btn.connect("clicked", self.on_copy_clicked)
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.direction_toggle.connect("toggled", self.on_direction_toggled)
        self.indents_spinner.connect("value-changed", self.on_indents_changed)
        self.input_textview.get_buffer().connect("changed", self.on_input_changed)

    def on_direction_toggled(self, data):
        self.direction = self.direction_toggle.get_active()
        self._convert()

    def on_indents_changed(self, data):
        self._convert()

    def on_input_changed(self, data):
        self._convert()

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("json2yaml")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("json2yaml")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("json2yaml")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("json2yaml")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_open_clicked(self, data):

        self._native = Gtk.FileChooserNative(
            title="Open File",
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel"
        )

        extensions = ["json", "yaml", "yml"]
        file_filter = Gtk.FileFilter()
        for f in extensions:
            file_filter.add_suffix(f)
        file_filter.set_name(_('JSON & YAML Files'))
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
        if JSON2YAML.is_text(contents[1]):
            text = contents[1].decode("utf-8")
        else:
            path = file.peek_path()
            self.toast.add_toast(
                Adw.Toast(title=_(f"{path}: Not a supported text file")))
            return

        # Insert in textview
        buffer = self.input_textview.get_buffer()
        buffer.set_text(text)
        buffer.place_cursor(buffer.get_end_iter())

        # Call convertion function
        self._convert()

    def on_paste_clicked(self, data):
        buffer = self.input_textview.get_buffer()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        buffer.paste_clipboard(clipboard, None, True)

    def on_clear_clicked(self, data):
        buffer = self.input_textview.get_buffer()
        buffer.set_text("")
        buffer = self.output_textview.get_buffer()
        buffer.set_text("")
        self.input_textview.remove_css_class("border-red")

    def on_copy_clicked(self, data):
        buffer = self.output_textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def _convert(self):

        self.input_textview.remove_css_class("border-red")

        input_buffer = self.input_textview.get_buffer()
        output_buffer = self.output_textview.get_buffer()
        input_text = input_buffer.get_text(
            input_buffer.get_start_iter(), input_buffer.get_end_iter(), False)
        indents = int(self.indents_spinner.get_value())

        # True: JSON to YAML, False: YAML to JSON
        if self.direction:
            if len(input_text) > 0 and JSON2YAML.is_json(input_text):
                output_buffer.set_text(JSON2YAML.to_yaml(input_text, indents))
            else:
                self.input_textview.add_css_class("border-red")
        else:
            if len(input_text) > 0 and JSON2YAML.is_yaml(input_text):
                output_buffer.set_text(JSON2YAML.to_json(input_text, indents))
            else:
                self.input_textview.add_css_class("border-red")
