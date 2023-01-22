# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GtkSource, Gdk
from gettext import gettext as _
from datetime import datetime
from dateutil import tz


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/timestamp.ui')
class TimestampView(Adw.Bin):
    __gtype_name__ = 'TimestampView'

    # Template elements
    _toast               = Gtk.Template.Child()
    _title               = Gtk.Template.Child()
    #_timezone_action_row = Gtk.Template.Child()
    _timestamp_spin_area = Gtk.Template.Child()
    _date_area           = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # timezone dropdown
        time = datetime.now(tz = tz.tzlocal())
        self._timestamp_spin_area.set_value(time.timestamp())
        self._date_area.set_date(time.year, time.month, time.day, time.hour, time.minute, time.second)



        # Signals
        self._timestamp_spin_area.connect("action-clicked", self._on_timestamp_now_clicked)
        self._timestamp_spin_area.connect("value-changed", self._on_timestamp_changed)
        self._date_area.connect("value-changed", self._on_date_changed)

    def _on_timestamp_now_clicked(self, data):
        self._timestamp_spin_area.set_value(int(datetime.now(tz = tz.tzlocal()).timestamp()))

    def _on_timestamp_changed(self, data):
        time = datetime.fromtimestamp(self._timestamp_spin_area.get_value())
        self._date_area.set_date(time.year, time.month, time.day, time.hour, time.minute, time.second)

    def _on_date_changed(self, data):
        year, month, day, hours, minutes, seconds = self._date_area.get_date()
        self._timestamp_spin_area.set_value(int(datetime(year, month, day, hour=hours, minute=minutes, second=seconds).timestamp()))
