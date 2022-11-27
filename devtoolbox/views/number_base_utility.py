# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gettext import gettext as _
from gi.repository import Gtk, Adw, Gio
from enum import Enum

from devtoolbox.services.number_base import Bases, NumberBase


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/number_base_utility.ui")
class NumberBaseUtility(Adw.Bin):
    __gtype_name__ = "NumberBaseUtility"

    toast = Gtk.Template.Child()
    #starred_btn = Gtk.Template.Child()
    decimal = Gtk.Template.Child()
    octal = Gtk.Template.Child()
    hex = Gtk.Template.Child()
    binary = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Favorites button icon
        #fav_list = self.settings.get_strv("favorites")
        #try:
        #    fav_list.index("baseconverter")  # check if present, throws error if not
            #self.starred_btn.set_icon_name("starred-symbolic")
        #except ValueError:
            #self.starred_btn.set_icon_name("non-starred-symbolic")
        #    pass

        # Signals
        self.decimal_handler_id = self.decimal.connect(
            "changed", self.on_decimal_change)
        self.octal_handler_id = self.octal.connect(
            "changed", self.on_octal_change)
        self.hex_handler_id = self.hex.connect("changed", self.on_hex_change)
        self.binary_handler_id = self.binary.connect(
            "changed", self.on_binary_change)
        #self.starred_btn.connect("clicked", self.on_star_clicked)
        #self.settings.connect("changed", self.on_settings_changed)

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            fav_list.index("baseconverter") # check if present, throws error if not
            #self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            #self.starred_btn.set_icon_name("non-starred-symbolic")
            pass

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            fav_list.index("baseconverter")  # check if present, throws error if not
            #self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("baseconverter")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            #self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("baseconverter")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_decimal_change(self, text):
        self._convert(Bases.DECIMAL)

    def on_octal_change(self, text):
        self._convert(Bases.OCTAL)

    def on_hex_change(self, text):
        self._convert(Bases.HEX)

    def on_binary_change(self, text):
        self._convert(Bases.BINARY)

    def _convert(self, input_base):
        self.binary.remove_css_class("border-red")
        self.octal.remove_css_class("border-red")
        self.decimal.remove_css_class("border-red")
        self.hex.remove_css_class("border-red")

        decimal_buffer = self.decimal.get_buffer()
        octal_buffer = self.octal.get_buffer()
        hex_buffer = self.hex.get_buffer()
        binary_buffer = self.binary.get_buffer()

        result = False
        numbers = []

        if input_base == Bases.BINARY:
            if NumberBase.is_binary(binary_buffer.get_text()):
                result, *numbers = NumberBase.convert(binary_buffer.get_text(), input_base)
            else:
                self.binary.add_css_class("border-red")
                return

        if input_base == Bases.OCTAL:
            if NumberBase.is_octal(octal_buffer.get_text()):
                result, *numbers = NumberBase.convert(octal_buffer.get_text(), input_base)
            else:
                self.octal.add_css_class("border-red")
                return

        if input_base == Bases.DECIMAL:
            if NumberBase.is_decimal(decimal_buffer.get_text()):
                result, *numbers = NumberBase.convert(decimal_buffer.get_text(), input_base)
            else:
                self.decimal.add_css_class("border-red")
                return

        if input_base == Bases.HEX:
            if NumberBase.is_hexadecimal(hex_buffer.get_text()):
                result, *numbers = NumberBase.convert(hex_buffer.get_text(), input_base)
            else:
                self.hex.add_css_class("border-red")
                return

        # Block signal to prevent infinite recursion
        self.decimal.handler_block(self.decimal_handler_id)
        self.octal.handler_block(self.octal_handler_id)
        self.hex.handler_block(self.hex_handler_id)
        self.binary.handler_block(self.binary_handler_id)
        
        # Display result
        if result:
            binary_buffer.set_text(numbers[0], -1)
            octal_buffer.set_text(numbers[1], -1)
            decimal_buffer.set_text(numbers[2], -1)
            hex_buffer.set_text(numbers[3], -1)

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
