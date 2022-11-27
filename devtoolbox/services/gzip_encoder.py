# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import binascii
import gzip
from gi.repository import Gdk, GLib


class GZipEncoder():
    
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
    def compress_text(text):
        return base64.b64encode(gzip.compress(text.encode())).decode("utf-8")

    @staticmethod
    def compress_image(image):
        return base64.b64encode(gzip.compress(image)).decode("utf-8")

    @staticmethod
    def decompress(input):
        try:
            return True, gzip.decompress(base64.b64decode(input))
        except binascii.Error:
            return False, ""