# converters_page.py
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


from gettext import gettext as _
from gi.repository import Gtk, Adw

from devtoolbox.widgets.sidebar_element import SidebarElement
import devtoolbox.params as params


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/utilities_view.ui")
class UtilitiesView(Adw.Bin):
    __gtype_name__ = "UtilitiesView"

    sidebar_stack = Gtk.Template.Child()
    sidebar = Gtk.Template.Child()

    def __init__(self, utilities):
        super().__init__()

        # Populate sidebar with pages
        for u in utilities:
            self.sidebar.append(
                SidebarElement(u, utilities[u]["title"], utilities[u]["icon-name"]))
            self.sidebar_stack.add_named(
                Gtk.Label(label=utilities[u]["title"]), u)
        self.sidebar.select_row(self.sidebar.get_first_child())

        # Signals
        self.sidebar.connect("row-activated", self.__change_page)

    def __change_page(self, widget, row):
        try:
            self.sidebar_stack.set_visible_child_name(row.get_page_name())
        except:
            pass
