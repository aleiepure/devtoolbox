# window.py
#
# Copyright 2023 Alessandro
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
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/window.ui')
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DevtoolboxWindow'

    _textarea = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._textarea.custom_file_extensions = ["iso"]

        self._textarea.connect("action-clicked", self._on_action_clicked),
        self._textarea.connect("text-changed", self._on_text_changed)
        self._textarea.connect("view-cleared", self._on_view_cleared)
        self._textarea.connect("text-loaded", self._on_text_loaded)
        self._textarea.connect("big-file", self._on_big_file)
        self._textarea.connect("error", self._on_error)

    def _on_action_clicked(self, data):
        print("Action!")

    def _on_text_changed(self, data):
        print("change")

    def _on_view_cleared(self, data):
        print("clear")

    def _on_text_loaded(self, data):
        print("loaded")

    def _on_big_file(self, data):
        print("big file")

    def _on_error(self, data, error):
        print(f"error: {error}")



    
