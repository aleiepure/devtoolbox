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

from gi.repository import Adw, Gtk, Gio


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/window.ui')
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DevtoolboxWindow'

    # Template elements
    _flap_btn = Gtk.Template.Child()
    _flap     = Gtk.Template.Child()
    _stack    = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        categories = {
            "favorites": {
                "title": _("Favorites"),
                "icon-name": "starred",
                "child": Gtk.Label(label="Favorites")
            },
            "converters": {
                "title": _("Converters"),
                "icon-name": "horizontal-arrows-symbolic",
                "child": Gtk.Label(label="Converters")
            },
            "encoders": {
                "title": _("Encoders"),
                "icon-name": "folder-templates-symbolic",
                "child": Gtk.Label(label="Encoders")
            },
            "formatters": {
                "title": _("Formatters"),
                "icon-name": "text-indent-symbolic",
                "child": Gtk.Label(label="Formatters")
            },
            "generators": {
                "title": _("Generators"),
                "icon-name": "plus-symbolic",
                "child": Gtk.Label(label="Generators")
            },
            "text": {
                "title": _("Text"),
                "icon-name": "text-ab-symbolic",
                "child": Gtk.Label(label="Text")
            },
            "graphics": {
                "title": _("Graphics"),
                "icon-name": "brush-symbolic",
                "child": Gtk.Label(label="Graphics")
            }
        }

        # Setup tabs
        for t in categories:
            self._stack.add_named(categories[t]["child"], t)
            page = self._stack.get_page(categories[t]["child"])
            page.set_title(categories[t]["title"])
            page.set_icon_name(categories[t]["icon-name"])

        # Signals
        self._flap_btn.connect("toggled", self._on_flap_btn_clicked)
        self.connect("close-request", self._on_close_request)

        # Restore last state
        self._settings.bind("window-width",     self, "default-width",  Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-height",    self, "default-height", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-maximized", self, "maximized",      Gio.SettingsBindFlags.DEFAULT)
        self._stack.set_visible_child_name(self._settings.get_string("last-tab"))
        # if self._stack.get_visible_child_name() != "favorites":
        #     self._stack.get_visible_child()._sidebar_stack.set_visible_child_name(
        #         self._settings.get_string("last-utility"))
        #     for i in range(0, 10):
        #             row = self._stack.get_visible_child()._sidebar.get_row_at_index(i)
        #             if row != None and row.get_page_name() == self._settings.get_string("last-utility"):
        #                 self._stack.get_visible_child().sidebar.select_row(row)


    def _on_flap_btn_clicked(self, data):
        self._flap.set_reveal_flap(self._flap_btn.get_active())

    def _on_close_request(self, data):
        tab = self._stack.get_visible_child_name()
        # if tab != "favorites":
        #     utility = self.tab_stack.get_visible_child().sidebar_stack.get_visible_child_name()
        #     self.settings.set_string("last-utility", utility)
        self._settings.set_string("last-tab", tab)

    
