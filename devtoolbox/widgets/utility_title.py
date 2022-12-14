# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from email.policy import default
from gi.repository import Gtk, Adw, GObject, Gio
from gettext import gettext as _


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/utility_title.ui')
class UtilityTitle(Adw.Bin):
    __gtype_name__ = "UtilityTitle"

    _title = Gtk.Template.Child()
    _description = Gtk.Template.Child()
    _starred_btn = Gtk.Template.Child()
   
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    title = GObject.Property(type=str, default="",
                             flags=GObject.ParamFlags.READWRITE)
    description = GObject.Property(type=str, default="",
                                   flags=GObject.ParamFlags.READWRITE)
    utility_name = GObject.Property(
        type=str, default="", flags=GObject.ParamFlags.READWRITE)

    __gsignals__ = {
        "added-favorite": (GObject.SIGNAL_RUN_LAST, None, ()),
        "removed-favorite": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self):
        super().__init__()

        # Button icon
        fav_list = self._settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index(self.utility_name)
            self._starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self._starred_btn.set_icon_name("non-starred-symbolic")

        # Property binding
        self.bind_property("title", self._title, "label",
                           GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("description", self._description,
                           "label", GObject.BindingFlags.SYNC_CREATE)

        # Signals
        self._starred_btn.connect("clicked", self.on_star_clicked)
        self._settings.connect("changed", self.on_settings_changed)

    def on_settings_changed(self, key, data):
        # Favorites button icon
        fav_list = self._settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index(self.utility_name)
            self._starred_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self._starred_btn.set_icon_name("non-starred-symbolic")

    def on_star_clicked(self, data):
        fav_list = self._settings.get_strv("favorites")
        try:
            # check if present, throws error if not
            fav_list.index(self.utility_name)
            self._starred_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove(self.utility_name)
            self._settings.set_strv("favorites", fav_list)
            self.emit("removed-favorite")
            # self.toast.add_toast(Adw.Toast(title=_("Removed from favorites!")))
        except ValueError:
            self._starred_btn.set_icon_name("starred-symbolic")
            fav_list.append(self.utility_name)
            self._settings.set_strv("favorites", fav_list)
            self.emit("added-favorite")
            # self.toast.add_toast(Adw.Toast(title=_("Added to favorites!")))

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_utility_name(self, utility_name):
        self.utility_name = utility_name

    def get_utility_name(self):
        return self.utility_name