# timestamp_utility.py
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

from datetime import datetime
from gettext import gettext as _
from gi.repository import Gtk, Adw


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/timestamp_utility.ui")
class TimestampUtility(Adw.Bin):
    __gtype_name__ = "TimestampUtility"

    starred_btn = Gtk.Template.Child()
    convert_btn = Gtk.Template.Child()
    now_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    convertDate_btn = Gtk.Template.Child()
    nowDate_btn = Gtk.Template.Child()
    clearDate_btn = Gtk.Template.Child()
    timestamp_spinner = Gtk.Template.Child()
    year_spinner = Gtk.Template.Child()
    month_spinner = Gtk.Template.Child()
    day_spinner = Gtk.Template.Child()
    hours_spinner = Gtk.Template.Child()
    minutes_spinner = Gtk.Template.Child()
    seconds_spinner = Gtk.Template.Child()
    #timezone_combo = Gtk.Template.Child()
    #timezone_combo_model = Gtk.Template.Child()
    #action_row = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # TODO: add favorites logic to button
        # self.starred_btn.set_icon_name("non-starred")

        # Populate timezone list
        #model = Gtk.StringList()
        # model = Gtk.ListStore(GObject.GType(Timezone))
        # for tz in pytz.common_timezones:
        #     timezone = Timezone(_(tz))
        #     #print(timezone)
        #     model.append(timezone)
        #     #model.append(_(tz))
        # dropdown = Gtk.DropDown()
        # dropdown.set_model(model)
        # #dropdown.set_enable_search(True)
        # #dropdown.set_expression(Gtk.PropertyExpression.new(Gtk.Label, None, "label"))
        # expression = Gtk.PropertyExpression(GObject.GType(Timezone), None, "name")
        # dropdown.set_expression(expression)
        # dropdown.set_enable_search(True)
        # #print(dropdown.get_expression())
        # self.action_row.add_suffix(dropdown)

        # Connect button signals
        self.convert_btn.connect("clicked", self.on_convert_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.now_btn.connect("clicked", self.on_now_clicked)
        self.convertDate_btn.connect("clicked", self.on_convertDate_clicked)
        self.nowDate_btn.connect("clicked", self.on_nowDate_clicked)
        self.clearDate_btn.connect("clicked", self.on_clearDate_clicked)

    def on_convert_clicked(self, widget):
        time = datetime.fromtimestamp(self.timestamp_spinner.get_value())
        self.year_spinner.set_value(time.year)
        self.month_spinner.set_value(time.month)
        self.day_spinner.set_value(time.day)
        self.hours_spinner.set_value(time.hour)
        self.minutes_spinner.set_value(time.minute)
        self.seconds_spinner.set_value(time.second)

    def on_clear_clicked(self, widget):
        self.timestamp_spinner.set_value(0)

    def on_now_clicked(self, widget):
        self.timestamp_spinner.set_value(datetime.now().timestamp())
        pass

    def on_convertDate_clicked(self, widget):
        year = int(self.year_spinner.get_value())
        month = int(self.month_spinner.get_value())
        day = int(self.day_spinner.get_value())
        hour = int(self.hours_spinner.get_value())
        minute = int(self.minutes_spinner.get_value())
        second = int(self.seconds_spinner.get_value())
        self.timestamp_spinner.set_value(datetime(year, month, day, hour, minute, second).timestamp())

    def on_clearDate_clicked(self, widget):
        self.year_spinner.set_value(1970)
        self.month_spinner.set_value(1)
        self.day_spinner.set_value(1)
        self.hours_spinner.set_value(0)
        self.minutes_spinner.set_value(0)
        self.seconds_spinner.set_value(0)

    def on_nowDate_clicked(self, widget):
        current_time = datetime.now()
        self.year_spinner.set_value(current_time.year)
        self.month_spinner.set_value(current_time.month)
        self.day_spinner.set_value(current_time.day)
        self.hours_spinner.set_value(current_time.hour)
        self.minutes_spinner.set_value(current_time.minute)
        self.seconds_spinner.set_value(current_time.second)
