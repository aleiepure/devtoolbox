# hash_generator_utility.py
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

from gi.repository import Adw, Gtk, Gio, Gdk, GLib
from gettext import gettext as _

from devtoolbox.service.hash_generator import HashGenerator
from devtoolbox.service.number_base import Bases, NumberBase
from devtoolbox.utils import Utils


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/hash_generator_utility.ui")
class HashGeneratorUtility(Adw.Bin):
    __gtype_name__ = "HashGeneratorUtility"

    toast = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    uppercase_switch = Gtk.Template.Child()
    format_dropdown = Gtk.Template.Child()
    input_stack = Gtk.Template.Child()
    input_text = Gtk.Template.Child()
    input_image = Gtk.Template.Child()
    input_file = Gtk.Template.Child()
    input_file_path_label = Gtk.Template.Child()
    open_btn = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    md5_text = Gtk.Template.Child()
    md5_copy_btn = Gtk.Template.Child()
    sha1_text = Gtk.Template.Child()
    sha1_copy_btn = Gtk.Template.Child()
    sha256_text = Gtk.Template.Child()
    sha256_copy_btn = Gtk.Template.Child()
    sha512_text = Gtk.Template.Child()
    sha512_copy_btn = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("hashgen")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Signals
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.uppercase_switch.connect(
            "notify::active", self.on_uppercase_state_changed)
        self.format_dropdown.connect(
            "notify::selected-item", self.on_format_dropdown_changed)
        self.input_text.get_buffer().connect("changed", self.on_input_text_changed)
        self.open_btn.connect("clicked", self.on_open_clicked)
        self.paste_btn.connect("clicked", self.on_paste_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.md5_copy_btn.connect("clicked", self.on_md5_copy_clicked)
        self.sha1_copy_btn.connect("clicked", self.on_sha1_copy_clicked)
        self.sha256_copy_btn.connect("clicked", self.on_sha256_copy_clicked)
        self.sha512_copy_btn.connect("clicked", self.on_sha512_copy_clicked)

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("hashgen")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("hashgen")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("hashgen")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("hashgen")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

    def on_uppercase_state_changed(self, state, data):
        self.generate_hash()

    def on_format_dropdown_changed(self, param_spec, data):
        self.generate_hash()

    def on_input_text_changed(self, data):
        self.generate_hash()

    def on_open_clicked(self, data):
        self._native = Gtk.FileChooserNative(
            title="Open File",
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel"
        )

        # File filters
        all_file_filter = Gtk.FileFilter()
        all_file_filter.add_pattern("*")
        all_file_filter.set_name(_("All files"))

        text_file_filter = Gtk.FileFilter()
        text_file_filter.add_mime_type("text/*")
        text_file_filter.set_name(_("Text files"))

        image_file_filter = Gtk.FileFilter()
        image_file_filter.add_pixbuf_formats()
        image_file_filter.set_name(_("Image files"))

        self._native.add_filter(all_file_filter)
        self._native.add_filter(text_file_filter)
        self._native.add_filter(image_file_filter)

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

        # Check if file is valid
        if not contents[0]:
            print(f"Unable to open {file.peek_path()}: {contents[1]}")
            return

        # Determine file type
        if Utils.is_text(contents[1]):
            self.input_type = "text"
            text = contents[1].decode("utf-8")
        elif Utils.is_image(contents[1]):
            self.input_type = "image"
            self.image_bytes = contents[1]
            texture = Gdk.Texture.new_from_bytes(GLib.Bytes(contents[1]))
        else:
            self.path = file.peek_path()
            self.input_type = "file"

        # Display as correct type
        if self.input_type == "text":
            self.input_stack.set_visible_child_name("text-view")
            buffer = self.input_text.get_buffer()
            buffer.set_text(text)
            buffer.place_cursor(buffer.get_end_iter())
        elif self.input_type == "image":
            self.input_stack.set_visible_child_name("image-view")
            self.input_image.set_paintable(texture)
        else:
            self.input_stack.set_visible_child_name("file-view")
            self.input_file_path_label.set_label(self.path)

        # Call convertion
        self.generate_hash()

    def on_paste_clicked(self, data):
        self.input_stack.set_visible_child_name("text-view")
        buffer = self.input_text.get_buffer()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        buffer.paste_clipboard(clipboard, None, True)

    def on_clear_clicked(self, data):
        self.input_stack.set_visible_child_name("text-view")
        self.input_text.get_buffer().set_text("")
        self.path = ""
        self.image_bytes = []
        self.md5_text.get_buffer().set_text("", -1)
        self.sha1_text.get_buffer().set_text("", -1)
        self.sha256_text.get_buffer().set_text("", -1)
        self.sha512_text.get_buffer().set_text("", -1)

    def on_md5_copy_clicked(self, data):
        text = self.md5_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_sha1_copy_clicked(self, data):
        text = self.sha1_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_sha256_copy_clicked(self, data):
        text = self.sha256_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_sha512_copy_clicked(self, data):
        text = self.sha512_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def generate_hash(self):
        input_buffer = self.input_text.get_buffer()
        format_type = self.format_dropdown.get_selected()
        uppercase = self.uppercase_switch.get_active()

        md5_buffer = self.md5_text.get_buffer()
        sha1_buffer = self.sha1_text.get_buffer()
        sha256_buffer = self.sha256_text.get_buffer()
        sha512_buffer = self.sha512_text.get_buffer()

        input_text = input_buffer.get_text(input_buffer.get_start_iter(),
                                           input_buffer.get_end_iter(), False).encode("utf-8")

        if format_type == 0:
            # Hex
            md5 = HashGenerator.to_md5(input_text)
            sha1 = HashGenerator.to_sha1(input_text)
            sha256 = HashGenerator.to_sha256(input_text)
            sha512 = HashGenerator.to_sha512(input_text)

            if uppercase == True:
                md5 = md5.upper()
                sha1 = sha1.upper()
                sha256 = sha256.upper()
                sha512 = sha512.upper()

        if format_type == 1:
            # Binary
            md5 = NumberBase.convert(
                HashGenerator.to_md5(input_text), Bases.HEX)[1]
            sha1 = NumberBase.convert(
                HashGenerator.to_sha1(input_text), Bases.HEX)[1]
            sha256 = NumberBase.convert(
                HashGenerator.to_sha256(input_text), Bases.HEX)[1]
            sha512 = NumberBase.convert(
                HashGenerator.to_sha512(input_text), Bases.HEX)[1]

            if uppercase == True:
                md5 = md5.upper()
                sha1 = sha1.upper()
                sha256 = sha256.upper()
                sha512 = sha512.upper()

        if format_type == 2:
            # Decimal
            md5 = NumberBase.convert(
                HashGenerator.to_md5(input_text), Bases.HEX)[3]
            sha1 = NumberBase.convert(
                HashGenerator.to_sha1(input_text), Bases.HEX)[3]
            sha256 = NumberBase.convert(
                HashGenerator.to_sha256(input_text), Bases.HEX)[3]
            sha512 = NumberBase.convert(
                HashGenerator.to_sha512(input_text), Bases.HEX)[3]

            if uppercase == True:
                md5 = md5.upper()
                sha1 = sha1.upper()
                sha256 = sha256.upper()
                sha512 = sha512.upper()

        md5_buffer.set_text(md5, -1)
        sha1_buffer.set_text(sha1, -1)
        sha256_buffer.set_text(sha256, -1)
        sha512_buffer.set_text(sha512, -1)
