# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject
from datetime import datetime
from dateutil import tz as timez
from zoneinfo import ZoneInfo
from pytz import all_timezones
from tzlocal import get_localzone_name
from gettext import gettext as _


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/timestamp.ui')
class TimestampView(Adw.Bin):
    __gtype_name__ = 'TimestampView'

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _tool_options = Gtk.Template.Child()
    # _timezone_comborow = Gtk.Template.Child()
    _timestamp_spin_area = Gtk.Template.Child()
    _date_area = Gtk.Template.Child()
    _iso_date = Gtk.Template.Child()
    _rfc2822_date = Gtk.Template.Child()
    _short_date = Gtk.Template.Child()
    _short_time = Gtk.Template.Child()
    _long_date = Gtk.Template.Child()
    _long_time = Gtk.Template.Child()
    _full_long_date = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Timezone dropdown
        self._timezone_comborow = self._create_dropdown()
        self._tool_options.add(self._timezone_comborow)

        # Set current date/time
        tz = get_localzone_name()

        # Fix for https://github.com/aleiepure/devtoolbox/issues/28
        if tz == "Europe/Kiev":
            tz = "Europe/Kyiv"

        self._timezone_comborow.set_selected(all_timezones.index(tz))
        time = datetime.now(tz=ZoneInfo(tz))
        self._timestamp_spin_area.set_value(time.timestamp())
        self._date_area.set_date(
            time.year, time.month, time.day, time.hour, time.minute, time.second)
        self._iso_date.set_text(time.isoformat("T"))
        self._rfc2822_date.set_text(time.strftime("%a, %d %b %Y %H:%M:%S %z"))
        self._short_date.set_text(time.strftime("%x"))
        self._short_time.set_text(time.strftime("%X"))
        self._long_date.set_text(time.strftime("%B %d %Y"))
        self._long_time.set_text(time.strftime("%I:%M:%S %p"))
        self._full_long_date.set_text(
            time.strftime("%A, %B %d %Y %I:%M:%S %p %Z"))

        # Signals
        self._timestamp_spin_area.connect(
            "action-clicked", self._on_timestamp_now_clicked)
        self._timestamp_spin_area.connect(
            "value-changed", self._on_timestamp_changed)
        self._date_area.connect("now-clicked", self._on_date_now_clicked)
        self._date_area.connect("value-changed", self._on_date_changed)
        self._timezone_comborow.connect(
            "notify::selected-item", self._on_changed_timezone)

    def _create_dropdown(self) -> Gtk.Widget:
        string_list_items = "\n".ljust(11).join(
            [f"<item>{time_zone}</item>" for time_zone in all_timezones]
        )

        title = _("Timezone")
        subtitle = _("Select the desired timezone")
        dropdown_ui = f"""<interface>
<object class="AdwComboRow" id="drop-down">
    <property name="title">{title}</property>
    <property name="subtitle">{subtitle}</property>
    <property name="icon-name">clock-alt-symbolic</property>
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
  </object>
</interface>"""

        builder = Gtk.Builder.new_from_string(dropdown_ui, -1)
        return builder.get_object("drop-down")

    def _on_changed_timezone(self, param_spec, data):
        self._on_timestamp_changed(None)
        self._on_date_changed(None)

    def _on_timestamp_now_clicked(self, source_widget: GObject.Object):
        tz = self._timezone_comborow.get_selected_item().get_string()
        date_time = datetime.now(tz=ZoneInfo(tz))
        self._timestamp_spin_area.set_value(int(date_time.timestamp()))
        self._iso_date.set_text(date_time.isoformat("T"))

    def _on_date_now_clicked(self, source_widget: GObject.Object):
        tz = self._timezone_comborow.get_selected_item().get_string()
        time = datetime.now(tz=ZoneInfo(tz))
        self._date_area.set_date(
            time.year, time.month, time.day, time.hour, time.minute, time.second)

    def _on_timestamp_changed(self, source_widget: GObject.Object):
        tz = self._timezone_comborow.get_selected_item().get_string()
        time = datetime.fromtimestamp(
            self._timestamp_spin_area.get_value(), tz=ZoneInfo(tz))
        self._date_area.set_date(
            time.year, time.month, time.day, time.hour, time.minute, time.second)
        self._iso_date.set_text(time.isoformat("T"))
        self._rfc2822_date.set_text(time.strftime("%a, %d %b %Y %H:%M:%S %z"))
        self._short_date.set_text(time.strftime("%x"))
        self._short_time.set_text(time.strftime("%X"))
        self._long_date.set_text(time.strftime("%B %d %Y"))
        self._long_time.set_text(time.strftime("%I:%M:%S %p"))
        self._full_long_date.set_text(
            time.strftime("%A, %B %d %Y %I:%M:%S %p %Z"))

    def _on_date_changed(self, source_widget: GObject.Object):
        tz = self._timezone_comborow.get_selected_item().get_string()
        year, month, day, hours, minutes, seconds = self._date_area.get_date()
        self._timestamp_spin_area.set_value(int(datetime(
            year, month, day, hour=hours, minute=minutes, second=seconds, tzinfo=ZoneInfo(tz)).timestamp()))
        self._iso_date.set_text(datetime(year, month, day, hour=hours,
                                minute=minutes, second=seconds, tzinfo=ZoneInfo(tz)).isoformat("T"))
        self._rfc2822_date.set_text(datetime(year, month, day, hour=hours, minute=minutes,
                                    second=seconds, tzinfo=ZoneInfo(tz)).strftime("%a, %d %b %Y %H:%M:%S %z"))
        self._short_date.set_text(datetime(year, month, day, hour=hours,
                                  minute=minutes, second=seconds, tzinfo=ZoneInfo(tz)).strftime("%x"))
        self._short_time.set_text(datetime(year, month, day, hour=hours,
                                  minute=minutes, second=seconds, tzinfo=ZoneInfo(tz)).strftime("%X"))
        self._long_date.set_text(datetime(year, month, day, hour=hours, minute=minutes,
                                 second=seconds, tzinfo=ZoneInfo(tz)).strftime("%B %d %Y"))
        self._long_time.set_text(datetime(year, month, day, hour=hours, minute=minutes,
                                 second=seconds, tzinfo=ZoneInfo(tz)).strftime("%I:%M:%S %p"))
        self._full_long_date.set_text(datetime(year, month, day, hour=hours, minute=minutes,
                                      second=seconds, tzinfo=ZoneInfo(tz)).strftime("%A, %B %d %Y %I:%M:%S %p %Z"))
