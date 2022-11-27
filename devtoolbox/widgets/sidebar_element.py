# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk


class SidebarElement(Gtk.ListBoxRow):

    def __init__(self, page_name, page_title, page_icon_name):
        super().__init__()

        self.page_name = page_name
        self.page_title = page_title
        self.page_icon_name = page_icon_name

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_margin_top(12)
        grid.set_margin_bottom(12)
        grid.set_margin_start(6)
        grid.set_margin_end(6)
        grid.set_column_spacing(12)

        icon = Gtk.Image()
        icon.set_from_icon_name(self.page_icon_name)
        grid.attach(icon, 0, 0, 1, 1)
        grid.attach(Gtk.Label(label=self.page_title, xalign=0.0), 1, 0, 1, 1)
        self.set_child(grid)

    def get_page_name(self):
        return self.page_name
