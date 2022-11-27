# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gettext import gettext as _
from gi.repository import Gtk, Adw

from devtoolbox.widgets.sidebar_element import SidebarElement


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/utilities_view.ui")
class UtilitiesView(Adw.Bin):
    __gtype_name__ = "UtilitiesView"

    sidebar_stack = Gtk.Template.Child()
    sidebar = Gtk.Template.Child()

    def __init__(self, utilities):
        super().__init__()

        # Populate sidebar with pages
        if len(utilities) != 0:
            for u in utilities:
                self.sidebar.append(
                    SidebarElement(u, utilities[u]["title"], utilities[u]["icon-name"]))
                self.sidebar_stack.add_named(utilities[u]["child"], u)
            self.sidebar.select_row(self.sidebar.get_first_child())

        # Signals
        self.sidebar.connect("row-activated", self.on_change_page)

    def on_change_page(self, widget, row):
        self.sidebar_stack.set_visible_child_name(row.get_page_name())