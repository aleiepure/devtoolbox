# Copyright (C) 2022-2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gdk, GLib
import json
from ruamel import yaml


class Utils():

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
    def is_json(input):
        try:
            json.loads(input)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def is_yaml(input):
        try:
            yaml.load(input, Loader=yaml.Loader)
            return True
        except yaml.YAMLError:
            return False
