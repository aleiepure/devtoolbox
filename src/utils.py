# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gdk, GLib
import ruamel.yaml
from enum import Enum
from lxml import etree
from crontab import CronSlices
import math
import json
import base64
import jwt
import re
from jsonschema.protocols import Validator
from jsonschema.exceptions import SchemaError


class Bases(Enum):
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEX = 16


class Utils:
    @staticmethod
    def is_text(test_input) -> bool:
        if isinstance(test_input, str):
            return True
        else:
            try:
                test_input.decode("utf-8")
                return True
            except UnicodeError:
                return False

    @staticmethod
    def is_image(test_input) -> bool:
        try:
            Gdk.Texture.new_from_bytes(GLib.Bytes(test_input))
            return True
        except GLib.GError:
            return False

    @staticmethod
    def is_json(test_input) -> bool:
        try:
            json.loads(test_input)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def is_yaml(test_input) -> bool:
        try:
            yaml = ruamel.yaml.YAML(typ='rt')
            yaml.load(test_input)
            return True
        except ruamel.yaml.YAMLError:
            return False

    @staticmethod
    def is_binary(number) -> bool:
        try:
            int(number, Bases.BINARY.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_octal(number) -> bool:
        try:
            int(number, Bases.OCTAL.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_decimal(number) -> bool:
        try:
            int(number, Bases.DECIMAL.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_hex(number) -> bool:
        try:
            int(number, Bases.HEX.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_cron_expression_valid(expression:str) -> bool:
        return CronSlices.is_valid(expression)

    @staticmethod
    def is_base64(text:str) -> bool:
        try:
            base64.b64decode(text)
            return True
        except Exception:
            return False

    @staticmethod
    def is_base64url(text:str) -> bool:
        try:
            base64.urlsafe_b64decode(text)
            return True
        except Exception:
            return False

    @staticmethod
    def is_jwt_token(token:str) -> bool:
        try:
            jwt.decode(token, options={"verify_signature": False})
            return True
        except Exception:
            return False

    @staticmethod
    def is_regex(regex:str) -> bool:
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

    @staticmethod
    def format_decimal(value: float, decimals: int = 2) -> str:
        return f"{value:.{decimals}f}".rstrip('0').rstrip('.')

    @staticmethod
    def normalized_to_uint8(value: float) -> int:
        if value < 0 or value > 1.0:
            raise ValueError("value must be between 0 and 1")
        return round(value * 255.0)

    @staticmethod
    def normalized_to_uintn(value: float, bits: int) -> int:
        if value < 0 or value > 1.0:
            raise ValueError("value must be between 0 and 1")
        if bits < 1:
            raise ValueError("bits must be atleast 1")
        return round(value * (2 ** bits - 1))

    @staticmethod
    def uintn_to_normalized(value: int, bits: int) -> float:
        max_value = (2 ** bits) - 1
        if value < 0 or value > max_value:
            raise ValueError("value must be between 0 and 2^bits-1")
        if bits < 1:
            raise ValueError("bits must be atleast 1")
        return value / max_value

    @staticmethod
    def normalized_to_percent(value: float) -> float:
        if value < 0 or value > 1.0:
            raise ValueError("value must be between 0 and 1")
        return value * 100.0

    @staticmethod
    def percent_to_normalized(value: float) -> float:
        if value < 0 or value > 100.0:
            raise ValueError("value must be between 0 and 100")
        return value / 100.0

    @staticmethod
    def normalized_to_deg(value: float) -> float:
        if value < 0.0 or value > 1.0:
            raise ValueError("value must be between 0.0 and 1.0")
        return value * 360.0

    @staticmethod
    def deg_to_normalized(value: float) -> float:
        value %= 360.0
        return value / 360.0

    @staticmethod
    def normalized_to_rad(value: float) -> float:
        if value < 0.0 or value > 1.0:
            raise ValueError("value must be between 0.0 and 1.0")
        return value * math.pi * 2.0

    @staticmethod
    def rad_to_normalized(value: float) -> float:
        value %= math.pi * 2.0
        return value / (math.pi * 2.0)

    @staticmethod
    def normalized_to_grad(value: float) -> float:
        if value < 0.0 or value > 1.0:
            raise ValueError("value must be between 0.0 and 1.0")
        return value * 400.0

    @staticmethod
    def grad_to_normalized(value: float) -> float:
        value %= 400.0
        return value / 400.0

    @staticmethod
    def is_numeric_chmod(value: int) -> bool:
        return (len(str(value)) <= 4 and
                all(digit in "01234567" for digit in str(value)))

    @staticmethod
    def is_symbolic_chmod(value: str) -> bool:
        if len(value) != 9:
            return False

        string = list(value)
        if (string[0] in ['-', 'r'] and
            string[1] in ['-', 'w'] and
            string[2] in ['-', 'x', 's', 'S'] and
            string[3] in ['-', 'r'] and
            string[4] in ['-', 'w'] and
            string[5] in ['-', 'x', 's', 'S'] and
            string[6] in ['-', 'r'] and
            string[7] in ['-', 'w'] and
            string[8] in ['-', 'x', 't', 'T']):
            return True
        else:
            return False

    @staticmethod
    def is_json_schema(text: str) -> bool:
        try:
            Validator.check_schema(json.loads(text))
            return True
        except:
            return False
