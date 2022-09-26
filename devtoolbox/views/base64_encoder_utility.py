# base64_encoder_utility.py
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

from devtoolbox.utils import Utils
from devtoolbox.services.base64_encoder import Base64Encoder


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/base64_encoder_utility.ui")
class Base64EncoderUtility(Adw.Bin):
    __gtype_name__ = "Base64EncoderUtility"

    toast = Gtk.Template.Child()
    encode_direction_toggle = Gtk.Template.Child()
    input_area = Gtk.Template.Child()
    output_area = Gtk.Template.Child()

    encode_direction = True  # True: encode, False: decode

    def __init__(self):
        super().__init__()

        # Signals
        self.encode_direction_toggle.connect(
            "toggled", self.on_encode_direction_toggled)
        self.input_area.connect("text-loaded", self.on_loaded)
        self.input_area.connect("image-loaded", self.on_loaded)
        self.input_area.connect("view-cleared", self.on_view_cleared)
        self.input_area.connect("text-changed", self.on_text_changed)
        self.input_area.connect("error", self.on_error)
        self.output_area.connect("error", self.on_error)

    def on_encode_direction_toggled(self, data):
        self.encode_direction = self.encode_direction_toggle.get_active()
        self._convert()

    def on_error(self, error):
        self.toast.add_toast(Adw.Toast(title=f"Error: {error}"))

    def on_view_cleared(self, data):
        self.output_area.clear()
        self.output_area.enable_copy(True)

    def on_loaded(self, data):
        self._convert()

    def on_text_changed(self, data):
        self._convert()

    def _convert(self):
        # True: encode, False: decode
        if self.encode_direction:
            if self.input_area.get_visible_view() == "text":
                text = self.input_area.get_text()
                self.output_area.get_buffer().set_text(Base64Encoder.encode_text(text))
            else:
                if len(self.input_area.get_image()) > 0:
                    self.output_area.get_buffer().set_text(
                        Base64Encoder.encode_image(self.input_area.get_image()))
        else:
            if self.input_area.get_visible_view() == "text":
                result, decoded_data = Base64Encoder.decode(
                    self.input_area.get_text())
                if result:
                    if Utils.is_text(decoded_data):
                        self.output_area.get_buffer().set_text(decoded_data.decode("utf-8"))
                        self.output_area.set_visible_view("text")
                    elif Utils.is_image(decoded_data):
                        texture = Gdk.Texture.new_from_bytes(
                            GLib.Bytes(decoded_data))
                        self.output_area.set_image(texture)
                else:
                    self.input_area.add_css_class("border-red")
            else:
                self.toast.add_toast(
                    Adw.Toast(title=_("Cannot decode from an image")))
                self.input_area.add_css_class("border-red")
