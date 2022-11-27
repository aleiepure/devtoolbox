# Copyright (C) 2022 Alessandro Iepure
# 
# SPDX-License-Identifier: GPL-3.0-or-later

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