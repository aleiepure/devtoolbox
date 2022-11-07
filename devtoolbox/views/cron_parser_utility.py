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

    toast = Gtk.Template.Child()
    dates_spinner = Gtk.Template.Child()
    format_text = Gtk.Template.Child()
    input_area = Gtk.Template.Child()
    output_area = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Signals
        self.input_area.connect("text-changed", self.on_input_changed)
        self.input_area.connect("view-cleared", self.on_view_cleared)
        self.input_area.connect("error", self.on_error)
        self.output_area.connect("error", self.on_error)
        self.dates_spinner.connect(
            "value-changed", self.on_dates_spinner_value_changed)
        self.format_text.connect("changed", self.on_format_change)

    def on_error(self, error):
        self.toast.add_toast(Adw.Toast(title=f"Error: {error}"))

    def on_view_cleared(self, data):
        self.output_area.clear()

    def on_dates_spinner_value_changed(self, data):
        self._generate_dates()

    def on_format_change(self, data):
        self.format_text.remove_css_class("border-red")
        if CronParser.is_date_format_valid(self.format_text.get_text()):
            self._generate_dates()
        else:
            self.format_text.add_css_class("border-red")

    def on_input_changed(self, data):
        self.input_area.remove_css_class("border-red")

        expression = self.input_area.get_text()
        if len(expression) > 0:
            if CronParser.is_expression_valid(expression):
                self._generate_dates()
            else:
                self.input_area.add_css_class("border-red")

    def _generate_dates(self):
        self.output_area.set_text(
            CronParser.generate_dates(
                self.input_area.get_text(),
                self.format_text.get_text(),
                int(self.dates_spinner.get_value())
            )
        )
