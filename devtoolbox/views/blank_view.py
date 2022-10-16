# blank_view.py
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

# TEMPLATE ONLY, NOT TO BE USED

from gi.repository import Adw, Gtk
from gettext import gettext as _


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/file_name.ui")
class BlankView(Adw.Bin):
    __gtype_name__ = "BlankView"

    # UI components
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._title.connect("added-favorite", self._on_added_favorite)
        self._title.connect("removed-favorite", self._on_removed_favorite)
    
    def _on_added_favorite(self, widget):
        self._toast.add_toast(Adw.Toast(title="Added to favorites!"))

    def _on_removed_favorite(self, widget):
        self._toast.add_toast(Adw.Toast(title="Removed from favorites!"))

    def _on_error(self, error):
        self._toast.add_toast(Adw.Toast(title=f"Error: {error}"))