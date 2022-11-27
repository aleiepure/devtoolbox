# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
from gettext import gettext as _
from gi.repository import Gtk, Adw, Gio
from pytz import common_timezones
from zoneinfo import ZoneInfo


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/timestamp_utility.ui")
class TimestampUtility(Adw.Bin):
    __gtype_name__ = "TimestampUtility"

    toast = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    now_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    nowDate_btn = Gtk.Template.Child()
    clearDate_btn = Gtk.Template.Child()
    timestamp_spinner = Gtk.Template.Child()
    year_spinner = Gtk.Template.Child()
    month_spinner = Gtk.Template.Child()
    day_spinner = Gtk.Template.Child()
    hours_spinner = Gtk.Template.Child()
    minutes_spinner = Gtk.Template.Child()
    seconds_spinner = Gtk.Template.Child()
    action_row = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("timestamp")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

        # Populate timezone list
        self.timezone_dropdown = self.create_drop_down()
        self.action_row.add_suffix(self.timezone_dropdown)

        # Connect button signals
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.now_btn.connect("clicked", self.on_now_clicked)
        self.nowDate_btn.connect("clicked", self.on_nowDate_clicked)
        self.clearDate_btn.connect("clicked", self.on_clearDate_clicked)
        self.starred_btn.connect("clicked", self.on_star_clicked)
        self.settings.connect("changed", self.on_settings_changed)
        self.timestamp_spinner.connect(
            "value-changed", self.on_timestamp_changed)
        self.year_spinner.connect("value-changed", self.on_date_changed)
        self.month_spinner.connect("value-changed", self.on_date_changed)
        self.day_spinner.connect("value-changed", self.on_date_changed)
        self.hours_spinner.connect("value-changed", self.on_date_changed)
        self.minutes_spinner.connect("value-changed", self.on_date_changed)
        self.seconds_spinner.connect("value-changed", self.on_date_changed)
        self.timezone_dropdown.connect("notify::selected-item", self.on_changed_timezone)

    def on_changed_timezone(self, param_spec, data):
        self.on_timestamp_changed(None)

    def create_drop_down(self):
        string_list_items = "\n".ljust(11).join(
            [f"<item>{time_zone}</item>" for time_zone in common_timezones]
        )

        drop_down_ui_string = f"""<interface>
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
  </object>
</interface>"""

        builder = Gtk.Builder.new_from_string(drop_down_ui_string, -1)
        drop_down = builder.get_object("drop-down")

        return drop_down

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("timestamp")
            self.starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self.starred_btn.set_icon_name("non-starred-symbolic")

    def on_star_clicked(self, data):
        fav_list = self.settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index("timestamp")
            self.starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove("timestamp")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self.starred_btn.set_icon_name("starred-symbolic")
            fav_list.append("timestamp")
            self.settings.set_strv("favorites", fav_list)
            self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def on_timestamp_changed(self, data):
        tz = self.timezone_dropdown.get_selected_item().get_string()
        time = datetime.fromtimestamp(
            self.timestamp_spinner.get_value(), tz=ZoneInfo(tz))
        self.year_spinner.set_value(time.year)
        self.month_spinner.set_value(time.month)
        self.day_spinner.set_value(time.day)
        self.hours_spinner.set_value(time.hour)
        self.minutes_spinner.set_value(time.minute)
        self.seconds_spinner.set_value(time.second)

    def on_clear_clicked(self, data):
        self.timestamp_spinner.set_value(0)

    def on_now_clicked(self, data):
        tz = self.timezone_dropdown.get_selected_item().get_string()
        self.timestamp_spinner.set_value(datetime.now(tz=ZoneInfo(tz)).timestamp())

    def on_date_changed(self, data):
        year = int(self.year_spinner.get_value())
        month = int(self.month_spinner.get_value())
        day = int(self.day_spinner.get_value())
        hour = int(self.hours_spinner.get_value())
        minute = int(self.minutes_spinner.get_value())
        second = int(self.seconds_spinner.get_value())
        tz = self.timezone_dropdown.get_selected_item().get_string()
        timestamp = datetime(year, month, day, hour=hour, minute=minute,
                             second=second, tzinfo=ZoneInfo(tz)).timestamp()
        self.timestamp_spinner.set_value(timestamp)

    def on_clearDate_clicked(self, data):
        self.year_spinner.set_value(1970)
        self.month_spinner.set_value(1)
        self.day_spinner.set_value(1)
        self.hours_spinner.set_value(0)
        self.minutes_spinner.set_value(0)
        self.seconds_spinner.set_value(0)

    def on_nowDate_clicked(self, data):
        tz = self.timezone_dropdown.get_selected_item().get_string()
        current_time = datetime.now(tz=ZoneInfo(tz))
        self.year_spinner.set_value(current_time.year)
        self.month_spinner.set_value(current_time.month)
        self.day_spinner.set_value(current_time.day)
        self.hours_spinner.set_value(current_time.hour)
        self.minutes_spinner.set_value(current_time.minute)
        self.seconds_spinner.set_value(current_time.second)
