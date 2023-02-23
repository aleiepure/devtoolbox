# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk
from gettext import gettext as _
from datetime import datetime
from dateutil import tz


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/date_area.ui')
class DateArea(Adw.Bin):
    __gtype_name__ = 'DateArea'

    # Template elements
    _name_lbl = Gtk.Template.Child()
    _now_btn = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _year_spinner = Gtk.Template.Child()
    _month_spinner = Gtk.Template.Child()
    _day_spinner = Gtk.Template.Child()
    _hours_spinner = Gtk.Template.Child()
    _minutes_spinner = Gtk.Template.Child()
    _seconds_spinner = Gtk.Template.Child()

    # Properties
    name = GObject.Property(type=str, default="")

    # Custom signals
    __gsignals__ = {
        "now-clicked":   (GObject.SIGNAL_RUN_LAST, None, ()),
        "value-changed": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "datearea")

        # Property binding
        self.bind_property("name", self._name_lbl, "label", GObject.BindingFlags.SYNC_CREATE)

        # Signal connection
        self._now_btn.connect("clicked", self._on_now_clicked)
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._year_spinner.connect("value-changed", self._on_value_changed)
        self._month_spinner.connect("value-changed", self._on_value_changed)
        self._day_spinner.connect("value-changed", self._on_value_changed)
        self._hours_spinner.connect("value-changed", self._on_value_changed)
        self._minutes_spinner.connect("value-changed", self._on_value_changed)
        self._seconds_spinner.connect("value-changed", self._on_value_changed)

    def _on_now_clicked(self, user_data:GObject.GPointer):
        date = datetime.now(tz = tz.tzlocal())
        self._year_spinner.set_value(date.year)
        self._month_spinner.set_value(date.month)
        self._day_spinner.set_value(date.day)
        self._hours_spinner.set_value(date.hour)
        self._minutes_spinner.set_value(date.minute)
        self._seconds_spinner.set_value(date.second)

    def _on_copy_clicked(self, user_data:GObject.GPointer):
        year = int(self._year_spinner.get_value())
        month = int(self._month_spinner.get_value())
        day = int(self._day_spinner.get_value())
        hours = int(self._hours_spinner.get_value())
        minutes = int(self._minutes_spinner.get_value())
        seconds = int(self._seconds_spinner.get_value())
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(str(datetime(year, month, day, hour=hours, minute=minutes, second=seconds)))

    def _on_value_changed(self,  user_data:GObject.GPointer):
        self.emit("value-changed")

    def get_date(self):
        year = int(self._year_spinner.get_value())
        month = int(self._month_spinner.get_value())
        day = int(self._day_spinner.get_value())
        hours = int(self._hours_spinner.get_value())
        minutes = int(self._minutes_spinner.get_value())
        seconds = int(self._seconds_spinner.get_value())
        return year, month, day, hours, minutes, seconds

    def set_date(self, year:int, month:int, day:int, hours:int, minutes:int, seconds:int):
        self._year_spinner.set_value(year)
        self._month_spinner.set_value(month)
        self._day_spinner.set_value(day)
        self._hours_spinner.set_value(hours)
        self._minutes_spinner.set_value(minutes)
        self._seconds_spinner.set_value(seconds)
