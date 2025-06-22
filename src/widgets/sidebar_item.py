# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, GObject, Pango


class SidebarItem(Gtk.ListBoxRow):
    __gtype_name__ = "SidebarItem"

    # Properties
    tool_name = GObject.Property(type=str, default="")
    title = GObject.Property(type=str, default="")
    icon_name = GObject.Property(type=str, default="")
    tool_tip = GObject.Property(type=str, default="")
    category = GObject.Property(type=str, default="")

    def __init__(self, tool_name: str, title: str, icon_name: str, tool_tip: str, category: str):
        super().__init__()

        self.tool_name = tool_name
        self.title = title
        self.icon_name = icon_name
        self.tool_tip = tool_tip
        self.category = category

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_margin_top(12)
        grid.set_margin_bottom(12)
        grid.set_margin_start(6)
        grid.set_margin_end(6)
        grid.set_column_spacing(12)

        icon = Gtk.Image()
        icon.set_from_icon_name(self.icon_name)
        grid.attach(icon, 0, 0, 1, 1)
        grid.attach(Gtk.Label(
            label=self.title,
            xalign=0.0,
            lines=2,
            wrap=True,
            ellipsize=Pango.EllipsizeMode.END
        ), 1, 0, 1, 1)
        self.set_child(grid)
        self.set_tooltip_text(self.tool_tip)

    def get_tool_name(self) -> str:
        return self.tool_name

    def get_title(self) -> str:
        return self.title

    def get_icon_name(self) -> str:
        return self.icon_name

    def get_tool_tip(self) -> str:
        return self.tool_tip

    def get_category(self) -> str:
        return self.category
