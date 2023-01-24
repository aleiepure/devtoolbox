# Copyright (C) 2022-2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gdk, GLib
from ruamel import yaml
from enum import Enum
from crontab import CronTab, CronSlices
import json


class Bases(Enum):
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEX = 16


class Utils:
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

    @staticmethod
    def is_binary(number):
        try:
            int(number, Bases.BINARY.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_octal(number):
        try:
            int(number, Bases.OCTAL.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_decimal(number):
        try:
            int(number, Bases.DECIMAL.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_hex(number):
        try:
            int(number, Bases.HEX.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_cron_expression_valid(expression: str):
        return CronSlices.is_valid(expression)
