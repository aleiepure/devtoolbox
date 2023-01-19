# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio
from gettext import gettext as _

@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/utility_title.ui')
class UtilityTitle(Adw.Bin):
    __gtype_name__ = 'UtilityTitle'

    # Template elements
    _title_lbl       = Gtk.Template.Child()
    _description_lbl = Gtk.Template.Child()
    _star_btn        = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    # Properties
    title        = GObject.Property(type=str, default="", flags=GObject.ParamFlags.READWRITE)
    description  = GObject.Property(type=str, default="", flags=GObject.ParamFlags.READWRITE)
    utility_name = GObject.Property(type=str, default="", flags=GObject.ParamFlags.READWRITE)

    # Custom signals
    __gsignals__ = {
        "added-favorite":   (GObject.SIGNAL_RUN_LAST, None, ()),
        "removed-favorite": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self,):
        super().__init__()

        # Check button icon
        self._set_btn_icon()

        # Property binding
        self.bind_property("title", self._title_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("description", self._description_lbl, "label", GObject.BindingFlags.SYNC_CREATE)

        # Signal connection
        self._star_btn.connect("clicked", self._on_star_clicked)
        self._settings.connect("changed", self._on_settings_changed)

    def _on_star_clicked(self, data):
        fav_list = self._settings.get_strv("favorites")
        try:
            fav_list.index(self.utility_name)
            self._star_btn.set_icon_name("non-starred-symbolic")
            fav_list.remove(self.utility_name)
            self._settings.set_strv("favorites", fav_list)
            self.emit("removed-favorite")
        except ValueError:
            self._star_btn.set_icon_name("starred-symbolic")
            fav_list.append(self.utility_name)
            self._settings.set_strv("favorites", fav_list)
            self.emit("added-favorite")

    def _on_settings_changed(self, key, data):
        self._set_btn_icon()

    def _set_btn_icon(self):
        fav_list = self._settings.get_strv("favorites")
        try:
            fav_list.index(self.utility_name)
            self._star_btn.set_icon_name("starred-symbolic")
        except ValueError:
            self._star_btn.set_icon_name("non-starred-symbolic")

    def set_title(self, title):
        self._title_lbl = title

    def get_title(self) -> str:
        return self.title

    def set_description(self, description):
        self._description_lbl = description

    def get_description(self) -> str:
        return self.description

    def get_utility_name(self) -> str:
        return self.utility_name







                   
