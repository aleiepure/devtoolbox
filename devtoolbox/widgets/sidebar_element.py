# sidebar_element.py
#
# Copyright 2022 Alessandro Iepure
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
