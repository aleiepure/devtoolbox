# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, GObject
from gettext import gettext as _
import string
import random


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/random_generator.ui")
class RandomGeneratorView(Adw.Bin):
    __gtype_name__ = "RandomGeneratorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _string_length_spinner = Gtk.Template.Child()
    _string_uppercase_switch = Gtk.Template.Child()
    _string_lowercase_switch = Gtk.Template.Child()
    _string_numbers_switch = Gtk.Template.Child()
    _string_special_chars_switch = Gtk.Template.Child()
    _random_string_row = Gtk.Template.Child()
    _number_min_spinner = Gtk.Template.Child()
    _number_max_spinner = Gtk.Template.Child()
    _random_number_row = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Initial generation
        self._generate_string()
        self._generate_number()

        # Signals
        self._string_length_spinner.connect("notify::value", self._on_string_length_changed)
        self._string_uppercase_switch.connect("notify::active", self._on_string_option_changed)
        self._string_lowercase_switch.connect("notify::active", self._on_string_option_changed)
        self._string_numbers_switch.connect("notify::active", self._on_string_option_changed)
        self._string_special_chars_switch.connect("notify::active", self._on_string_option_changed)
        self._random_string_row.connect("generate-clicked", self._on_string_generate_again)
        self._number_min_spinner.connect("notify::value", self._on_number_bound_changed)
        self._number_max_spinner.connect("notify::value", self._on_number_bound_changed)
        self._random_number_row.connect("generate-clicked", self._on_number_generate_again)

    def _on_string_length_changed(self, pspec:GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate_string()

    def _on_string_option_changed(self, pspec:GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate_string()

    def _on_string_generate_again(self, widget:GObject.GPointer):
        self._generate_string()

    def _on_number_bound_changed(self, pspec:GObject.ParamSpec, user_data:GObject.GPointer):
        self._generate_number()

    def _on_number_generate_again(self, widget:Gtk.Widget):
        self._generate_number()

    def _generate_string(self):
        output = ""
        letters = ""

        if self._string_uppercase_switch.get_active():
            letters += string.ascii_uppercase
        if self._string_lowercase_switch.get_active():
            letters += string.ascii_lowercase
        if self._string_numbers_switch.get_active():
            letters += string.digits
        if self._string_special_chars_switch.get_active():
            letters += string.punctuation

        letters_list = list(letters)
        random.shuffle(letters_list)
        letters = "".join(letters_list)

        for i in range(0, int(self._string_length_spinner.get_value())):
            rnd = random.randint(0, len(letters)-1)
            output += letters[rnd]

        self._random_string_row.set_text(output)

    def _generate_number(self):
        rnd = random.randint(int(self._number_min_spinner.get_value()), int(self._number_max_spinner.get_value()))
        self._random_number_row.set_text(str(rnd))
