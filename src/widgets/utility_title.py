# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/utility_title.ui')
class UtilityTitle(Adw.Bin):
    __gtype_name__ = 'UtilityTitle'

    # Template elements
    _title_lbl = Gtk.Template.Child()
    _description_lbl = Gtk.Template.Child()

    # Properties
    title = GObject.Property(type=str, default="")
    description = GObject.Property(type=str, default="")
    tool_name = GObject.Property(type=str, default="")

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "utilitytitle")

        # Property binding
        self.bind_property("title", self._title_lbl, "label", GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property("description", self._description_lbl, "label", GObject.BindingFlags.BIDIRECTIONAL)

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
