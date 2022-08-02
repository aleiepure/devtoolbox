# number_base_utility.py
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
from gi.repository import Gtk, Adw
from enum import Enum


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/number_base_utility.ui")
class NumberBaseUtility(Adw.Bin):
    __gtype_name__ = "NumberBaseUtility"

    toast = Gtk.Template.Child()
    decimal = Gtk.Template.Child()
    octal = Gtk.Template.Child()
    hex = Gtk.Template.Child()
    binary = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Signals
        self.decimal_handler_id = self.decimal.connect(
            "changed", self.on_decimal_change)
        self.octal_handler_id = self.octal.connect(
            "changed", self.on_octal_change)
        self.hex_handler_id = self.hex.connect("changed", self.on_hex_change)
        self.binary_handler_id = self.binary.connect(
            "changed", self.on_binary_change)

    def on_decimal_change(self, text):
        self._convert(Bases.DECIMAL)

    def on_octal_change(self, text):
        self._convert(Bases.OCTAL)

    def on_hex_change(self, text):
        self._convert(Bases.HEX)

    def on_binary_change(self, text):
        self._convert(Bases.BINARY)

    def _convert(self, input_base):
        decimal_buffer = self.decimal.get_buffer()
        octal_buffer = self.octal.get_buffer()
        hex_buffer = self.hex.get_buffer()
        binary_buffer = self.binary.get_buffer()

        self.binary.remove_css_class("border-red")
        self.octal.remove_css_class("border-red")
        self.decimal.remove_css_class("border-red")
        self.hex.remove_css_class("border-red")

        match input_base:
            case Bases.BINARY:
                try:
                    decimal_num = int(
                        binary_buffer.get_text(), Bases.BINARY.value)
                except:
                    self.binary.add_css_class("border-red")
                    return
            case Bases.OCTAL:
                try:
                    decimal_num = int(
                        octal_buffer.get_text(), Bases.OCTAL.value)
                except:
                    self.octal.add_css_class("border-red")
                    return
            case Bases.DECIMAL:
                try:
                    decimal_num = int(
                        decimal_buffer.get_text(), Bases.DECIMAL.value)
                except:
                    self.decimal.add_css_class("border-red")
                    return
            case Bases.HEX:
                try:
                    decimal_num = int(hex_buffer.get_text(), Bases.HEX.value)
                except:
                    self.hex.add_css_class("border-red")
                    return

        octal_num = oct(decimal_num).replace("0o", "")
        hex_num = hex(decimal_num).replace("0x", "").upper()
        binary_num = bin(decimal_num).replace("0b", "")

        # Block signal to prevent infinite recursion
        self.decimal.handler_block(self.decimal_handler_id)
        self.octal.handler_block(self.octal_handler_id)
        self.hex.handler_block(self.hex_handler_id)
        self.binary.handler_block(self.binary_handler_id)

        decimal_buffer.set_text(str(decimal_num), len(str(decimal_num)))
        octal_buffer.set_text(octal_num, len(octal_num))
        hex_buffer.set_text(hex_num, len(hex_num))
        binary_buffer.set_text(binary_num, len(binary_num))
        
        # Move cursor at the end
        self.decimal.set_position(-1)
        self.octal.set_position(-1)
        self.hex.set_position(-1)
        self.binary.set_position(-1)

        # Unblock signals to allow future changes
        self.decimal.handler_unblock(self.decimal_handler_id)
        self.octal.handler_unblock(self.octal_handler_id)
        self.hex.handler_unblock(self.hex_handler_id)
        self.binary.handler_unblock(self.binary_handler_id)


class Bases(Enum):
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEX = 16
