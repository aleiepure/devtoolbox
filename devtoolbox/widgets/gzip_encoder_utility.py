# gzip_encoder_utility.py
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
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

from ..service.gzip_encoder import GZipEncoder


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/gzip_encoder_utility.ui")
class GZipEncoderUtility(Adw.Bin):
    __gtype_name__ = "GZipEncoderUtility"

    toast = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    compress_direction_toggle = Gtk.Template.Child()
    open_btn = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    input_type_stack = Gtk.Template.Child()
    input_textview = Gtk.Template.Child()
    input_image = Gtk.Template.Child()
    output_type_stack = Gtk.Template.Child()
    output_textview = Gtk.Template.Child()
    output_image = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    compress_direction = True  # True: compress, False: decompress
    input_is_text = True
    image_bytes = []

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("gzipencoder")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Signals
        self.compress_direction_toggle.connect(
            "toggled", self.on_compress_direction_toggled)
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.open_btn.connect("clicked", self.on_open_clicked)
        self.paste_btn.connect("clicked", self.on_paste_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.copy_btn.connect("clicked", self.on_copy_clicked)
        self.input_textview.get_buffer().connect("changed", self.on_text_changed)

    def on_compress_direction_toggled(self, data):
        self.compress_direction = self.compress_direction_toggle.get_active()
        self.output_type_stack.set_visible_child_name("text")
        self._convert()

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("gzipencoder")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("gzipencoder")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("gzipencoder")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("gzipencoder")
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
        all_file_filter = Gtk.FileFilter()
        all_file_filter.add_mime_type("text/*")
        all_file_filter.add_pixbuf_formats()
        all_file_filter.set_name(_("All supported files"))

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
            path = file.peek_path()
            print(f"Unable to open {path}: {contents[1]}")
            return

        # Determine file type
        if GZipEncoder.is_text(contents[1]):
            self.input_is_text = True
            text = contents[1].decode("utf-8")
        elif GZipEncoder.is_image(contents[1]):
            self.input_is_text = False
            self.image_bytes = contents[1]
            texture = Gdk.Texture.new_from_bytes(GLib.Bytes(contents[1]))
        else:
            path = file.peek_path()
            self.toast.add_toast(
                Adw.Toast(title=_(f"{path}: Not a supported text file")))
            return

        # Display file as text or image
        if self.input_is_text:
            self.input_type_stack.set_visible_child_name("text")
            buffer = self.input_textview.get_buffer()
            buffer.set_text(text)
            buffer.place_cursor(buffer.get_end_iter())
        else:
            self.input_type_stack.set_visible_child_name("image")
            self.input_image.set_paintable(texture)

        # Call convertion
        self._convert()

    def on_paste_clicked(self, data):
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        buffer = self.input_textview.get_buffer()
        buffer.paste_clipboard(clipboard, None, True)
        self.input_is_text = True

    def on_clear_clicked(self, data):
        self.input_type_stack.set_visible_child_name("text")
        self.output_type_stack.set_visible_child_name("text")
        buffer = self.input_textview.get_buffer()
        buffer.set_text("")
        buffer = self.output_textview.get_buffer()
        buffer.set_text("")
        self.input_is_text = True
        self.input_image.remove_css_class("border-red")
        self.input_textview.remove_css_class("border-red")
        self.copy_btn.set_sensitive(True)

    def on_copy_clicked(self, data):
        buffer = self.output_textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_text_changed(self, data):
        self._convert()

    def _convert(self):
        self.input_image.remove_css_class("border-red")
        self.copy_btn.set_sensitive(True)

        input_buffer = self.input_textview.get_buffer()
        input_text = input_buffer.get_text(
            input_buffer.get_start_iter(), input_buffer.get_end_iter(), False)
        output_buffer = self.output_textview.get_buffer()

        # True: compress, False: decompress
        if self.compress_direction:
            if len(input_text) > 0 and self.input_is_text:
                output_buffer.set_text(GZipEncoder.compress_text(input_text))
            else:
                output_buffer.set_text(
                    GZipEncoder.compress_image(self.image_bytes))

        else:
            if self.input_is_text:
                result, decompressed_data = GZipEncoder.decompress(input_text)
                if result:
                    if GZipEncoder.is_text(decompressed_data):
                        output_buffer.set_text(
                            decompressed_data.decode("utf-8"))
                        self.output_type_stack.set_visible_child_name("text")
                    elif GZipEncoder.is_image(decompressed_data):
                        texture = Gdk.Texture.new_from_bytes(
                            GLib.Bytes(decompressed_data))
                        self.output_image.set_paintable(texture)
                        self.output_type_stack.set_visible_child_name("image")
                        self.copy_btn.set_sensitive(False)
                else:
                    self.input_textview.add_css_class("border-red")
            else:
                self.toast.add_toast(
                    Adw.Toast(title=_("Cannot decompress from an image")))
                self.input_image.add_css_class("border-red")
