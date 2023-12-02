# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/utility_title.ui')
class UtilityTitle(Adw.Bin):
    __gtype_name__ = 'UtilityTitle'

    # Template elements
    _title_lbl = Gtk.Template.Child()
    _description_lbl = Gtk.Template.Child()
    _star_btn = Gtk.Template.Child()

    # Properties
    title = GObject.Property(type=str, default="")
    description = GObject.Property(type=str, default="")
    tool_name = GObject.Property(type=str, default="")

    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "utilitytitle")

        # Property binding
        self.bind_property("title", self._title_lbl, "label", GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property("description", self._description_lbl, "label", GObject.BindingFlags.BIDIRECTIONAL)

    @Gtk.Template.Callback()
    def _on_map(self, user_data: object | None) -> None:
        """
        Callback for "map" signal.
        Sets the star icon based on the current gsettings state.

        Args:
            user_data (object or None): additional data passed to the callback

        Returns:
            None
        """

        if self.tool_name in self._settings.get_strv('favorites'):
            self._star_btn.set_icon_name('starred')
        else:
             self._star_btn.set_icon_name('non-starred')

    @Gtk.Template.Callback()
    def _on_star_btn_clicked(self, user_data: object | None):
        """
        Callback for "clicked" signal.
        Changes the icon, updates gsettings and calls for a refresh of the
        favorites popover.

        Args:
            user_data (object or None): additional data passed to the callback

        Returns:
            None
        """

        favorites = self._settings.get_strv('favorites')
        if self.tool_name in favorites:
            self._star_btn.set_icon_name('non-starred')
            favorites.remove(self.tool_name)
            self._settings.set_strv('favorites', favorites)
        else:
            self._star_btn.set_icon_name('starred')
            favorites.append(self.tool_name)
            self._settings.set_strv('favorites', favorites)
        self.get_ancestor(Adw.ApplicationWindow).activate_action('win.refresh-favorites', None)

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
