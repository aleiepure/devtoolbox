# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/utility_title.ui')
class UtilityTitle(Adw.Bin):
    __gtype_name__ = 'UtilityTitle'

    # Template elements
    _title_lbl       = Gtk.Template.Child()
    _description_lbl = Gtk.Template.Child()
    # _star_btn        = Gtk.Template.Child()

    # GSettings
    # Feature not implemented
    # _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    # Properties
    title = GObject.Property(type=str, default="")
    description = GObject.Property(type=str, default="")
    tool_name = GObject.Property(type=str, default="")

    # Custom signals
    # Feature not implemented
    # __gsignals__ = {
    #     "added-favorite":   (GObject.SIGNAL_RUN_LAST, None, ()),
    #     "removed-favorite": (GObject.SIGNAL_RUN_LAST, None, ()),
    # }

    def __init__(self):
        super().__init__()

        # Property binding
        self.bind_property("title", self._title_lbl, "label", GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property("description", self._description_lbl, "label", GObject.BindingFlags.BIDIRECTIONAL)

        # Signal connection
        # Feature not implemented
        # self._star_btn.connect("clicked", self._on_star_btn_clicked)
        # self._settings.connect("changed::favorites", self._on_settings_changed)
        # self.connect("map", self._on_map)

    # Feature not implemented
    # def _on_map(self, data):
    #     self._set_star_btn_icon()

    # Feature not implemented
    # def _on_star_btn_clicked(self, data):
    #     fav_list = self._settings.get_strv("favorites")
    #     try:
    #         fav_list.index(self.tool_name)
    #         self._star_btn.set_icon_name("non-starred-symbolic")
    #         fav_list.remove(self.tool_name)
    #         self._settings.set_strv("favorites", fav_list)
    #         self.emit("removed-favorite")
    #     except ValueError:
    #         self._star_btn.set_icon_name("starred-symbolic")
    #         fav_list.append(self.tool_name)
    #         self._settings.set_strv("favorites", fav_list)
    #         self.emit("added-favorite")

    # Feature not implemented
    # def _on_settings_changed(self, key, data):
    #     self._set_star_btn_icon()

    # Feature not implemented
    # def _set_star_btn_icon(self):
    #     fav_list = self._settings.get_strv("favorites")
    #     try:
    #         fav_list.index(self.tool_name)
    #         self._star_btn.set_icon_name("starred-symbolic")
    #     except ValueError:
    #         self._star_btn.set_icon_name("non-starred-symbolic")

    def set_title(self, title:str):
        self.title = title

    def get_title(self) -> str:
        return self.title

    def set_description(self, description:str):
        self.description = description

    def get_description(self) -> str:
        return self.description

    def set_tool_name(self, tool_name:str):
        self.tool_name = tool_name

    def get_tool_name(self) -> str:
        return self.tool_name
