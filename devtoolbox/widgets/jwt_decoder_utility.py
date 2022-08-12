# jwt_decoder_utility.py
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

from textwrap import indent
import jwt
import json
from gi.repository import Gtk, Adw, Gio, Gdk
from gettext import gettext as _


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/jwt_decoder_utility.ui")
class JWTDecoderUtility(Adw.Bin):
    __gtype_name__ = "JWTDecoderUtility"

    toast = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    open_btn = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    token_textview = Gtk.Template.Child()
    header_textview = Gtk.Template.Child()
    payload_textview = Gtk.Template.Child()
    header_copy_btn = Gtk.Template.Child()
    payload_copy_btn = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("jwtdecoder")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Signals
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.open_btn.connect("clicked", self.on_open_clicked)
        self.paste_btn.connect("clicked", self.on_paste_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.header_copy_btn.connect("clicked", self.on_header_copy_clicked)
        self.payload_copy_btn.connect("clicked", self.on_payload_copy_clicked)
        self.token_textview.get_buffer().connect("changed", self.on_text_changed)

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("jwtdecoder")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("jwtdecoder")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("jwtdecoder")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("jwtdecoder")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

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

        # Signal
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

        if not contents[0]:
            path = file.peek_path()
            self.toast.add_toast(
                Adw.Toast(title=_(f"Error opening file {path}")))
            return

        try:
            text = contents[1].decode('utf-8')
        except UnicodeError:
            path = file.peek_path()
            self.toast.add_toast(
                Adw.Toast(title=_(f"{path}: Not a supported text file")))

        buffer = self.token_textview.get_buffer()
        buffer.set_text(text)
        buffer.place_cursor(buffer.get_end_iter())
        self._convert()

    def on_paste_clicked(self, widget):
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        buffer = self.token_textview.get_buffer()
        buffer.paste_clipboard(clipboard, None, True)

    def on_clear_clicked(self, widget):
        buffer = self.token_textview.get_buffer()
        buffer.set_text("")
        buffer = self.header_textview.get_buffer()
        buffer.set_text("")
        buffer = self.payload_textview.get_buffer()
        buffer.set_text("")
        self.token_textview.remove_css_class("border-red") 

    def on_header_copy_clicked(self, widget):
        buffer = self.header_textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_payload_copy_clicked(self, widget):
        buffer = self.payload_textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_text_changed(self, data):
        self._convert()

    def _convert(self):
        self.token_textview.remove_css_class("border-red") 
        input_buffer = self.token_textview.get_buffer()
        token = input_buffer.get_text(
            input_buffer.get_start_iter(), input_buffer.get_end_iter(), False)

        try:
            self.header_textview.get_buffer().set_text(json.dumps(jwt.get_unverified_header(token), indent=4))
            self.payload_textview.get_buffer().set_text(json.dumps(jwt.decode(token, options={"verify_signature": False}), indent=4))
        except jwt.exceptions.DecodeError:
            self.token_textview.add_css_class("border-red")
