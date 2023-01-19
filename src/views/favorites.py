# Copyright (C) 2022-2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gio
from gettext import gettext as _
from .tab_content import TabContent


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/empty-favorites.ui')
class EmptyFavorites(Adw.Bin):
    __gtype_name__ = "EmptyFavorites"

    _flap = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    def get_flap(self) -> Adw.Flap:
        return self._flap


class Favorites(Adw.Bin):

    _stack = Adw.ViewStack(vexpand=True)

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, tools):
        super().__init__()

        # Create the views
        self._empty_view = EmptyFavorites()
        self._filled_view = TabContent(self._get_favorite_tools(tools))

        # Add them to the stack
        self._stack.add_named(self._empty_view, "empty")
        self._stack.add_named(self._filled_view, "filled")

        # Determine the view to show
        favorites = self._settings.get_strv("favorites")
        if len(favorites) == 0:
            self._stack.set_visible_child_name("empty")
        else:
            self._stack.set_visible_child_name("filled")

        # Set the main child
        self.set_child(self._stack)

        # Signals
        self._settings.connect("changed", self._on_settings_changed, tools)

    def _on_settings_changed(self, key, data, tools):
        favorites = self._settings.get_strv("favorites")
        if len(favorites) == 0:
            self._stack.set_visible_child_name("empty")
        else:
            self._stack.remove(self.filled_view)
            self._filled_view = TabContent(self._get_favorite_tools(tools))
            self._stack.add_named(self._filled_view, "filled")
            self._stack.set_visible_child_name("filled")

    def _get_favorite_tools(self, tools):
        favorites_as_strings = self._settings.get_strv("favorites")
        favorites_as_objects = {title:tools[title] for title in favorites_as_strings}
        return favorites_as_objects

    def get_flap(self) -> Adw.Flap:
        return self._stack.get_visible_child().get_flap()



