# cron_parser_utility.py
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

from gi.repository import Gtk, Adw, Gdk, Gio
from ..services.cron_parser import CronParser


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/cron_parser_utility.ui")
class CronParserUtility(Adw.Bin):
    __gtype_name__ = "CronParserUtility"

    # star button logic
    dates_spinner = Gtk.Template.Child()
    format_text = Gtk.Template.Child()
    expression_text = Gtk.Template.Child()
    dates_text = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    toast = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("cronparser")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Signals
        self.paste_btn.connect("clicked", self.on_paste_btn_clicked)
        self.clear_btn.connect("clicked", self.on_clear_btn_clicked)
        self.copy_btn.connect("clicked", self.on_copy_btn_clicked)
        self.dates_spinner.connect(
            "value-changed", self.on_dates_spinner_value_changed)
        self.format_text.connect("changed", self.on_format_change)
        self.expression_text.connect("changed", self.on_expression_change)
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("cronparser")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("cronparser")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("cronparser")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("cronparser")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_dates_spinner_value_changed(self, data):
        self._generate_dates()

    def on_format_change(self, data):
        self.format_text.remove_css_class("border-red")
        if CronParser.is_date_format_valid(self.format_text.get_text()):
            self._generate_dates()
        else:
            self.format_text.add_css_class("border-red")

    def on_expression_change(self, data):
        self.expression_text.remove_css_class("border-red")

        expression = self.expression_text.get_text()
        if len(expression) > 0:
            if CronParser.is_expression_valid(expression):
                self._generate_dates()
            else:
                self.expression_text.add_css_class("border-red")
        
    def on_paste_btn_clicked(self, data):
        self.expression_text.emit("paste-clipboard")

    def on_clear_btn_clicked(self, data):
        buffer = self.expression_text.get_buffer()
        buffer.set_text("", -1)
        buffer = self.dates_text.get_buffer()
        buffer.set_text("", -1)

    def on_copy_btn_clicked(self, data):
        buffer = self.dates_text.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def _generate_dates(self):
        self.dates_text.get_buffer().set_text(
            CronParser.generate_dates(
                self.expression_text.get_text(),
                self.format_text.get_text(),
                int(self.dates_spinner.get_value())
            )
        )
