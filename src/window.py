# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GObject
from .widgets.sidebar_item import SidebarItem
from .views.tab_content import TabContent
from .views.favorites import Favorites


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/window.ui')
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DevtoolboxWindow'

    # Template elements
    _flap_btn   = Gtk.Template.Child()
    _tabs_stack = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        tools = {
            "json-yaml": {
                "title": _("JSON - YAML"),
                "category": "converter",
                "icon-name": "horizontal-arrows-symbolic",
                "child": Gtk.Label(label="Json - yaml")
            },
            "timestamp": {
                "title": _("Timestamp"),
                "category": "converter",
                "icon-name": "hourglass-symbolic",
                "child": Gtk.Label(label="Timestamp")
            },
            "encoder": {
                "title": _("Encoder"),
                "category": "encoder",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="Encoder")
            },
            "formatter": {
                "title": _("formatter"),
                "category": "formatter",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="formatter")
            },
            "generator": {
                "title": _("generator"),
                "category": "generator",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="generator")
            },
            "text": {
                "title": _("text"),
                "category": "text",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="text")
            },
            "graphic": {
                "title": _("graphic"),
                "category": "graphic",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="graphic")
            }
        }

        categories = {
            "favorite": {
                "title": _("Favorites"),
                "icon-name": "starred",
                "child": Favorites(tools)
            },
            "converter": {
                "title": _("Converters"),
                "icon-name": "horizontal-arrows-symbolic",
                "child": TabContent(self._get_tools(tools, "converter"))
            },
            "encoder": {
                "title": _("Encoders"),
                "icon-name": "folder-templates-symbolic",
                "child": TabContent(self._get_tools(tools, "encoder"))
            },
            "formatter": {
                "title": _("Formatters"),
                "icon-name": "text-indent-symbolic",
                "child": TabContent(self._get_tools(tools, "formatter"))
            },
            "generator": {
                "title": _("Generators"),
                "icon-name": "plus-symbolic",
                "child": TabContent(self._get_tools(tools, "generator"))
            },
            "text": {
                "title": _("Text"),
                "icon-name": "text-ab-symbolic",
                "child": TabContent(self._get_tools(tools, "text"))
            },
            "graphic": {
                "title": _("Graphics"),
                "icon-name": "brush-symbolic",
                "child": TabContent(self._get_tools(tools, "graphic"))
            }
        }

        # Setup tabs
        for c in categories:
            self._tabs_stack.add_named(categories[c]["child"], c)
            page = self._tabs_stack.get_page(categories[c]["child"])
            page.set_title(categories[c]["title"])
            page.set_icon_name(categories[c]["icon-name"])
            self._flap_btn.bind_property("active", page.get_child().get_flap(), "reveal_flap", GObject.BindingFlags.SYNC_CREATE)
            page.get_child().get_flap().bind_property("reveal_flap", self._flap_btn, "active", GObject.BindingFlags.SYNC_CREATE)

        # Restore last state
        self._settings.bind("window-width",     self, "default-width",  Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-height",    self, "default-height", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-maximized", self, "maximized",      Gio.SettingsBindFlags.DEFAULT)
        self._tabs_stack.set_visible_child_name(self._settings.get_string("last-tab"))
        self._flap_btn.set_active(self._settings.get_boolean("sidebar-open"))


        # Signals
        # self._flap_btn.connect("toggled", self._on_flap_btn_clicked)
        self.connect("close-request", self._on_close_request)

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
        tab = self._tabs_stack.get_visible_child_name()
        # if tab != "favorites":
        #     utility = self.tab_stack.get_visible_child().sidebar_stack.get_visible_child_name()
        #     self.settings.set_string("last-utility", utility)
        self._settings.set_string("last-tab", tab)
        self._settings.set_boolean("sidebar-open", self._flap_btn.get_active())

    def _get_tools(self, tools: dict, category: str):
        tools_in_category = {}
        for t in tools:
            if tools[t]["category"] == category:
                tools_in_category[t] = tools[t]
        return tools_in_category

    
