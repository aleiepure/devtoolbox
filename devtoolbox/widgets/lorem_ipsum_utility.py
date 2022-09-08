# lorem_ipsum_utility.py
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

from gi.repository import Adw, Gtk, Gio, Gdk
from gettext import gettext as _

from devtoolbox.service.lorem_ipsum_generator import LoremIpsumGenerator


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/lorem_ipsum_generator.ui")
class LoremIpsumUtility(Adw.Bin):
    __gtype_name__ = "LoremIpsumUtility"

    toast = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    begin_with_lorem_ipsum_switch = Gtk.Template.Child()
    type_dropdown = Gtk.Template.Child()
    amount_spinner = Gtk.Template.Child()
    output_text = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("loremipsum")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Signals
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.begin_with_lorem_ipsum_switch.connect(
            "state-set", self.on_begin_changed)
        self.type_dropdown.connect(
            "notify::selected-item", self.on_type_changed)
        self.amount_spinner.connect("value-changed", self.on_amount_changed)
        self.copy_btn.connect("clicked", self.on_copy_clicked)

        # Call generation
        self.generate_text()

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("loremipsum")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("loremipsum")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("loremipsum")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("loremipsum")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

    def on_begin_changed(self, state, data):
        self.output_text.get_buffer().set_text("")
        self.generate_text()

    def on_type_changed(self, param_spec, data):
        self.generate_text()

    def on_amount_changed(self, data):
        self.generate_text()

    def on_copy_clicked(self, data):
        buffer = self.output_text.get_buffer()
        text = buffer.get_text(buffer.get_start_iter(),
                               buffer.get_end_iter(), False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def generate_text(self):
        output_buffer = self.output_text.get_buffer()
        selected = self.type_dropdown.get_selected()
        amount = int(self.amount_spinner.get_value())
        start_str = "Lorem ipsum dolor sit amet, "
        if selected == 0:
            generated_str = LoremIpsumGenerator.generate_words(amount)
        if selected == 1:
            generated_str = LoremIpsumGenerator.generate_senctences(amount)
        if selected == 2:
            generated_str = LoremIpsumGenerator.generate_paragraphs(amount)

        if self.begin_with_lorem_ipsum_switch.get_active() == True:
            output_buffer.set_text(
                start_str + generated_str[0].lower()+generated_str[1:])
        else:
            output_buffer.set_text(generated_str)
