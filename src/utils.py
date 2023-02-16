# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gdk, GLib
from ruamel import yaml
from enum import Enum
from crontab import CronTab, CronSlices
import json
import base64
import binascii
import jwt
import re
from lxml import etree


class Bases(Enum):
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEX = 16


class Utils:
    @staticmethod
    def is_text(test_input):
        if isinstance(test_input, str):
            return True
        else:
            try:
                test_input.decode("utf-8")
                return True
            except UnicodeError:
                return False

    @staticmethod
    def is_image(test_input):
        try:
            Gdk.Texture.new_from_bytes(GLib.Bytes(test_input))
            return True
        except GLib.GError:
            return False

    @staticmethod
    def is_json(test_input):
        try:
            json.loads(test_input)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def is_yaml(test_input):
        try:
            yaml.load(test_input, Loader=yaml.Loader)
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

    @staticmethod
    def is_base64(text: str):
        try:
            base64.b64decode(text)
            return True
        except Exception:
            return False

    @staticmethod
    def is_jwt_token(token: str):
        try:
            jwt.decode(token, options={"verify_signature": False})
            return True
        except Exception:
            return False

    @staticmethod
    def is_regex(regex:str):
        try:
            re.compile(r"{}".format(regex))
            return True
        except re.error:
            return False

    @staticmethod
    def is_xml(text:str) -> bool:
        try:
            etree.fromstring(bytes(text, encoding="utf-8"))
            return True
        except etree.ParseError:
            return False

    def is_xsd(text:str) -> bool:
        try:
            parser = etree.XMLParser(no_network=False)
            schema_root = etree.fromstring(bytes(text, encoding="utf-8"), parser=parser)
            return True
        except Exception as e:
            print(e)
            return False
