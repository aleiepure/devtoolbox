# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, GObject, Adw, Gio
from ..widgets.sidebar_item import SidebarItem


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/tab_content.ui')
class TabContent(Adw.Bin):
    __gtype_name__ = "TabContent"

    # Template elements
    _flap          = Gtk.Template.Child()
    _sidebar       = Gtk.Template.Child()
    _content_stack = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, tools, category):
        super().__init__()

        # Populate sidebar
        for t in tools:
            self._sidebar.append(SidebarItem(name=t, title=tools[t]["title"], icon_name=tools[t]["icon-name"]))
            self._content_stack.add_named(tools[t]["child"], t)

        # Select the correct row
        try:
            if self._settings.get_string("last-tab") == category and len(tools) != 0:
                index = list(tools.keys()).index(self._settings.get_string("last-tool"))
                if index == 0:
                    self._sidebar.select_row(self._sidebar.get_first_child())
                else:
                    self._sidebar.select_row(self._sidebar.get_row_at_index(index))
            else:
                self._sidebar.select_row(self._sidebar.get_first_child())
        except ValueError:
            self._sidebar.select_row(self._sidebar.get_first_child())

        self._content_stack.set_visible_child_name(self._sidebar.get_selected_row().get_name())

        #self._settings.bind("last-tool", self._content_stack, "visible-child-name", Gio.SettingsBindFlags.DEFAULT)

        # Signals
        self._sidebar.connect("row-activated", self._on_sidebar_change)

    def _on_sidebar_change(self, widget, row):
        self._content_stack.set_visible_child_name(row.get_name())

    def get_flap(self) -> Adw.Flap:
        return self._flap

    def get_content_stack(self) -> Adw.ViewStack:
        return self._content_stack

    def set_sidebar_content(self, tools):
        self._set_sidebar_content(tools)
