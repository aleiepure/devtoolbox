# window.py
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

from devtoolbox.views.utilities_view import UtilitiesView
from devtoolbox.widgets.json2yaml_utility import Json2YamlUtility
from devtoolbox.widgets.timestamp_utility import TimestampUtility


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/main.ui")
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    main_content = Gtk.Template.Child()
    tab_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Adw.ApplicationWindow.__init__(self, **kwargs)

        # Populate stack
        CONVERTERS_UTILITIES = {
            "json2yaml": {
                "title": _("JSON - YAML"),
                "icon-name": "right-left-symbolic",
                "child": Json2YamlUtility()
            },
            "timestamp": {
                "title": _("Timestamp"),
                "icon-name": "clock-rotate-symbolic",
                "child": TimestampUtility()
            },
            "baseconverter": {
                "title": _("Number Base"),
                "icon-name": "hashtag-symbolic",
                "child": Gtk.Label(label="Number base")
            },
            "cronparser": {
                "title": _("Cron Parser"),
                "icon-name": "hourglass-half-symbolic",
                "child": Gtk.Label(label="Cron parser")
            }
        }
        TABS = {
            "favorites": {
                "title": _("Favorites"),
                "icon-name": "starred",
                "child": Gtk.Label(label="Favorites")
            },
            "converters": {
                "title": _("Converters"),
                "icon-name": "right-left-symbolic",
                "child": UtilitiesView(CONVERTERS_UTILITIES)
            },
            "encoders": {
                "title": _("Encoders"),
                "icon-name": "folder-templates-symbolic",
                "child": Gtk.Label(label="Encoders")
            },
            "formatters": {
                "title": _("Formatters"),
                "icon-name": "text-indent-more-symbolic",
                "child": Gtk.Label(label="Formatters")
            },
            "generators": {
                "title": _("Generators"),
                "icon-name": "plus-symbolic",
                "child": Gtk.Label(label="Generators")
            },
            "text": {
                "title": _("Text"),
                "icon-name": "text-symbolic",
                "child": Gtk.Label(label="Text")
            },
            "graphics": {
                "title": _("Graphics"),
                "icon-name": "applications-graphics-symbolic",
                "child": Gtk.Label(label="Graphics")
            }
        }
        for t in TABS:
            self.tab_stack.add_named(TABS[t]["child"], t)
            page = self.tab_stack.get_page(TABS[t]["child"])
            page.set_title(TABS[t]["title"])
            page.set_icon_name(TABS[t]["icon-name"])

        # set first selected tab
        self.tab_stack.set_visible_child_name("converters")
