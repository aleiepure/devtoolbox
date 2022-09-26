# number_base.py
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
