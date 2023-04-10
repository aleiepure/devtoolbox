# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject
from datetime import datetime
from dateutil import tz as timez
from zoneinfo import ZoneInfo
from pytz import common_timezones
from tzlocal import get_localzone_name


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/timestamp.ui')
class TimestampView(Adw.Bin):
    __gtype_name__ = 'TimestampView'

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _timezone_row = Gtk.Template.Child()
    _timestamp_spin_area = Gtk.Template.Child()
    _date_area = Gtk.Template.Child()
    _iso_date = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Timezone dropdown
        self._timezone_dropdown = self._create_dropdown()
        self._timezone_row.add_suffix(self._timezone_dropdown)

        # Set current date/time
        tz = get_localzone_name()
        self._timezone_dropdown.set_selected(common_timezones.index(tz))
        time = datetime.now(tz = ZoneInfo(tz))
        self._timestamp_spin_area.set_value(time.timestamp())
        self._date_area.set_date(time.year, time.month, time.day, time.hour, time.minute, time.second)
        self._iso_date.set_text(time.isoformat("T"))

        # Signals
        self._timestamp_spin_area.connect("action-clicked", self._on_timestamp_now_clicked)
        self._timestamp_spin_area.connect("value-changed", self._on_timestamp_changed)
        self._date_area.connect("now-clicked", self._on_date_now_clicked)
        self._date_area.connect("value-changed", self._on_date_changed)
        self._timezone_dropdown.connect("notify::selected-item", self._on_changed_timezone)

    def _create_dropdown(self):
        string_list_items = "\n".ljust(11).join(
            [f"<item>{time_zone}</item>" for time_zone in common_timezones]
        )

        dropdown_ui = f"""<interface>
  <object class="GtkDropDown" id="drop-down">
    <property name="model">
      <object class="GtkStringList">
        <items>
          {string_list_items}
        </items>
      </object>
    </property>
    <property name="enable-search">true</property>
    <property name="expression">
      <lookup type="GtkStringObject" name="string"></lookup>
    </property>
    <property name="valign">center</property>
    <property name="width-request">260</property>
  </object>
</interface>"""

        builder = Gtk.Builder.new_from_string(dropdown_ui, -1)
        return builder.get_object("drop-down")

    def _on_changed_timezone(self, param_spec, data):
        self._on_timestamp_changed(None)
        self._on_date_changed(None)

    def _on_timestamp_now_clicked(self, source_widget:GObject.Object):
        tz = self._timezone_dropdown.get_selected_item().get_string()
        date_time = datetime.now(tz=ZoneInfo(tz))
        self._timestamp_spin_area.set_value(int(date_time.timestamp()))
        self._iso_date.set_text(date_time.isoformat("T"))

    def _on_date_now_clicked(self, source_widget:GObject.Object):
        tz = self._timezone_dropdown.get_selected_item().get_string()
        time = datetime.now(tz=ZoneInfo(tz))
        self._date_area.set_date(time.year, time.month, time.day, time.hour, time.minute, time.second)

    def _on_timestamp_changed(self, source_widget:GObject.Object):
        tz = self._timezone_dropdown.get_selected_item().get_string()
        time = datetime.fromtimestamp(self._timestamp_spin_area.get_value(), tz=ZoneInfo(tz))
        self._date_area.set_date(time.year, time.month, time.day, time.hour, time.minute, time.second)
        self._iso_date.set_text(time.isoformat("T"))

    def _on_date_changed(self, source_widget:GObject.Object):
        tz = self._timezone_dropdown.get_selected_item().get_string()
        year, month, day, hours, minutes, seconds = self._date_area.get_date()
        self._timestamp_spin_area.set_value(int(datetime(year, month, day, hour=hours, minute=minutes, second=seconds, tzinfo=ZoneInfo(tz)).timestamp()))
        self._iso_date.set_text(datetime(year, month, day, hour=hours, minute=minutes, second=seconds, tzinfo=ZoneInfo(tz)).isoformat("T"))
