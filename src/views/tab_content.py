# Copyright (C) 2022-2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, GObject, Adw
from ..widgets.sidebar_item import SidebarItem


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/tab_content.ui')
class TabContent(Adw.Bin):
    __gtype_name__ = "TabContent"

    # Template elements
    _flap          = Gtk.Template.Child()
    _sidebar       = Gtk.Template.Child()
    _content_stack = Gtk.Template.Child()

    def __init__(self, tools):
        super().__init__()

        # Populate sidebar
        for t in tools:
            self._sidebar.append(SidebarItem(name=t, title=tools[t]["title"], icon_name=tools[t]["icon-name"]))
            self._content_stack.add_named(tools[t]["child"], t)
        self._sidebar.select_row(self._sidebar.get_first_child())

        # Signals
        self._sidebar.connect("row-activated", self._on_sidebar_change)

    def _on_sidebar_change(self, widget, row):
        self._content_stack.set_visible_child_name(row.get_name())

    def get_flap(self) -> Adw.Flap:
        return self._flap
