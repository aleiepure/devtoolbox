# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum


class Bases(Enum):
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEX = 16


class NumberBase():

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
    def is_hexadecimal(number):
        try:
            int(number, Bases.HEX.value)
            return True
        except ValueError:
            return False

    @staticmethod
    def convert(number, starting_base):
        if starting_base == Bases.BINARY:
            try:
                decimal_num = int(number, Bases.BINARY.value)
            except ValueError:
                return False, 0, 0, 0, 0
        if starting_base == Bases.OCTAL:
            try:
                decimal_num = int(number, Bases.OCTAL.value)
            except ValueError:
                return False, 0, 0, 0, 0
        if starting_base == Bases.DECIMAL:
            try:
                decimal_num = int(number, Bases.DECIMAL.value)
            except ValueError:
                return False, 0, 0, 0, 0
        if starting_base == Bases.HEX:
            try:
                decimal_num = int(number, Bases.HEX.value)
            except ValueError:
                return False, 0, 0, 0, 0

        octal_num = oct(decimal_num).replace("0o", "")
        hex_num = hex(decimal_num).replace("0x", "").upper()
        binary_num = bin(decimal_num).replace("0b", "")

        return True, binary_num, octal_num, str(decimal_num), hex_num
