# base64_encoder.py
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

import base64
import binascii
from gi.repository import Gdk, GLib

class Base64Encoder():

    @staticmethod
    def is_text(input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    @staticmethod
    def is_image(input):
        try:
            Gdk.Texture.new_from_bytes(GLib.Bytes(input))
            return True
        except GLib.GError:
            return False

    @staticmethod
    def encode_text(text):
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    @staticmethod
    def encode_image(image):
        return base64.b64encode(image).decode("utf-8")

    @staticmethod
    def decode(input):
        try:
            return True, base64.b64decode(input)
        except binascii.Error:
            return False, ""