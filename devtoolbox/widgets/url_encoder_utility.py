# url_encoder_utility.py
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
from gi.repository import Adw, Gtk, Gio, Gdk

from ..service.url_encoder import URLEncoder


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/url_encoder_utility.ui")
class UrlEncoderUtility(Adw.Bin):
    __gtype_name__ = "UrlEncoderUtility"

    toast = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    direction_encode = Gtk.Template.Child()
    direction_decode = Gtk.Template.Child()
    input_textview = Gtk.Template.Child()
    output_textview = Gtk.Template.Child()
    open_btn = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    space_as_plus_toggle = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("urlencoder")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # True: encode, False: decode
        self.direction = True

        # True: space as '+', False: space as '%20'
        self.space_as_plus = False

        # Signals
        self.open_btn.connect("clicked", self.on_open_clicked)
        self.paste_btn.connect("clicked", self.on_paste_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.copy_btn.connect("clicked", self.on_copy_clicked)
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.input_textview.get_buffer().connect("changed", self.on_text_changed)
        self.direction_encode.connect("toggled", self.on_direction_changed)
        self.space_as_plus_toggle.connect(
            "toggled", self.on_space_encoding_changed)

    def on_open_clicked(self, data):
        self._native = Gtk.FileChooserNative(
            title="Open File",
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel"
        )

        # File filters
        file_filter = Gtk.FileFilter()
        file_filter.add_mime_type("text/*")
        file_filter.set_name(_("Text files"))
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
        if URLEncoder.is_text(contents[1]):
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

    def on_paste_clicked(self, widget):
        buffer = self.input_textview.get_buffer()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        buffer.paste_clipboard(clipboard, None, True)

    def on_clear_clicked(self, widget):
        buffer = self.input_textview.get_buffer()
        buffer.set_text("")
        buffer = self.output_textview.get_buffer()
        buffer.set_text("")

    def on_copy_clicked(self, widget):
        buffer = self.output_textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("urlencoder")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("urlencoder")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("urlencoder")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("urlencoder")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

    def on_text_changed(self, data):
        self._convert()

    def on_direction_changed(self, data):
        self.direction = self.direction_encode.get_active()
        self._convert()

    def on_space_encoding_changed(self, data):
        self.space_as_plus = self.space_as_plus_toggle.get_active()
        self._convert()

    def _convert(self):
        input_buffer = self.input_textview.get_buffer()
        output_buffer = self.output_textview.get_buffer()
        input_text = input_buffer.get_text(
            input_buffer.get_start_iter(), input_buffer.get_end_iter(), False)
        # True: encode, False: decode
        if self.direction:
            output_buffer.set_text(URLEncoder.encode(
                input_text, self.space_as_plus))
        else:
            output_buffer.set_text(URLEncoder.decode(input_text))
