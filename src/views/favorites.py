# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gio
from gettext import gettext as _
from .tab_content import TabContent
from .json_yaml import JsonYamlView
import copy


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/empty_favorites.ui')
class EmptyFavorites(Adw.Bin):
    __gtype_name__ = "EmptyFavorites"

    _flap = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    def get_flap(self) -> Adw.Flap:
        return self._flap


class FavoritesView(Adw.Bin):

    _stack = Adw.ViewStack(vexpand=True)

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        # Create the views
        self._empty_view = EmptyFavorites()
        self._filled_view = TabContent(self._get_favorite_tools())

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
        self._settings.connect("changed", self._on_settings_changed)

    def _on_settings_changed(self, key, data):
        favorites = self._settings.get_strv("favorites")
        if len(favorites) == 0:
            self._stack.set_visible_child_name("empty")
        else:
            #self._stack.remove(self._filled_view)
            #self._filled_view = TabContent(self._get_favorite_tools())
            #self._stack.add_named(self._filled_view, "filled")
            self._filled_view.set_sidebar_content(self._get_favorite_tools())
            self._stack.set_visible_child_name("filled")

    def _get_favorite_tools(self):
        tools = {
            "json-yaml": {
                "title": _("JSON - YAML"),
                "category": "converter",
                "icon-name": "horizontal-arrows-symbolic",
                "child": JsonYamlView()
            },
            "timestamp": {
                "title": _("Timestamp"),
                "category": "converter",
                "icon-name": "hourglass-symbolic",
                "child": Gtk.Label(label="Timestamp")
            },
            "encoder": {
                "title": _("Encoder"),
                "category": "encoder",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="Encoder")
            },
            "formatter": {
                "title": _("formatter"),
                "category": "formatter",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="formatter")
            },
            "generator": {
                "title": _("generator"),
                "category": "generator",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="generator")
            },
            "text": {
                "title": _("text"),
                "category": "text",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="text")
            },
            "graphic": {
                "title": _("graphic"),
                "category": "graphic",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="graphic")
            }
        }
        favorites_as_strings = self._settings.get_strv("favorites")
        favorites_as_objects = {title: tools[title] for title in favorites_as_strings}
        return favorites_as_objects

    def get_filled_view_flap(self) -> Adw.Flap:
        return self._stack.get_child_by_name("filled").get_flap()

    def get_empty_view_flap(self) -> Adw.Flap:
        return self._stack.get_child_by_name("empty").get_flap()

    def get_content_stack(self) -> Adw.ViewStack:
        return self._filled_view.get_content_stack()



