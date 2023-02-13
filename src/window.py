# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GObject
from gettext import gettext as _

from .widgets.sidebar_item import SidebarItem

from .views.tab_content import TabContent
from .views.json_yaml import JsonYamlView
from .views.timestamp import TimestampView
from .views.base_converter import BaseConverterView
from .views.cron_converter import CronConverterView
from .views.html_encoder import HtmlEncoderView
from .views.url_encoder import UrlEncoderView
from .views.base64_encoder import Base64EncoderView
from .views.gzip_compressor import GzipCompressorView
from .views.jwt_decoder import JwtDecoderView
from .views.formatter import FormatterView
from .views.hash_generator import HashGeneratorView
from .views.lorem_generator import LoremGeneratorView
from .views.uuid_generator import UuidGeneratorView
from .views.text_inspector import TextInspectorView

from .formatters.json import JsonFormatter
from .formatters.sql import SqlFormatter
from .formatters.xml import XmlFormatter


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/window.ui")
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = "DevtoolboxWindow"

    # Template elements
    _title = Gtk.Template.Child()
    _flap_btn = Gtk.Template.Child()
    _tabs_stack = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, debug, **kwargs):
        super().__init__(**kwargs)

        # Theme headerbar
        if debug == "False":
            self.remove_css_class("devel")

        tools = {
            "json-yaml": {
                "title": _("JSON - YAML"),
                "category": "converter",
                "icon-name": "horizontal-arrows-symbolic",
                "tooltip": "Convert JSON documents to YAML and vice-versa",
                "child": JsonYamlView(),
            },
            "timestamp": {
                "title": _("Timestamp"),
                "category": "converter",
                "icon-name": "calendar-symbolic",
                "tooltip": "Convert UNIX timestamps to and from plain dates",
                "child": TimestampView(),
            },
            "placeholder5": {
                "title": _("placeholder5"),
                "category": "graphic",
                "icon-name": "clock-rotate-symbolic",
                "tooltip": "Placeholder",
                "child": Gtk.Label(label="graphic"),
            },
            "base-converter": {
                "title": _("Base converter"),
                "category": "converter",
                "icon-name": "hashtag-symbolic",
                "tooltip": "Convert numbers between common bases",
                "child": BaseConverterView(),
            },
            "cron": {
                "title": _("Cron converter"),
                "category": "converter",
                "icon-name": "hourglass-symbolic",
                "tooltip": "Interpret cron expressions to plain dates",
                "child": CronConverterView(),
            },
            "html-encoder": {
                "title": "HTML",
                "category": "encoder",
                "icon-name": "code-symbolic",
                "tooltip": "Encode and decode special characters using the HTML format",
                "child": HtmlEncoderView(),
            },
            "url-encoder": {
                "title": "URL",
                "category": "encoder",
                "icon-name": "chain-link-symbolic",
                "tooltip": "Encode and decode special characters inside URLs",
                "child": UrlEncoderView(),
            },
            # "base64-encoder": {
            #     "title": "Base64",
            #     "category": "encoder",
            #     "icon-name": "base64-symbolic",
            #     "tooltip": "Encode and decode files and texts using base64",
            #     "child": Base64EncoderView(),
            # },
            "gzip-compressor": {
                "title": "GZip",
                "category": "encoder",
                "icon-name": "shoe-box-symbolic",
                "tooltip": "Compress and decompress files and texts using gzip",
                "child": GzipCompressorView(),
            },
            "jwt-decoder": {
                "title": "JWT",
                "category": "encoder",
                "icon-name": "key-symbolic",
                "tooltip": "Decode JWT tokens with ease",
                "child": JwtDecoderView(),
            },
            "json-formatter": {
                "title": "JSON",
                "category": "formatter",
                "icon-name": "json-symbolic",
                "tooltip": _("Format JSON documents"),
                "child": FormatterView(JsonFormatter()),
            },
            "sql-formatter": {
                "title": "SQL",
                "category": "formatter",
                "icon-name": "database-symbolic",
                "tooltip": _("Format SQL documents"),
                "child": FormatterView(SqlFormatter()),
            },
            "xml-formatter": {
                "title": "XML",
                "category": "formatter",
                "icon-name": "code-symbolic",
                "tooltip": _("Format XML documents"),
                "child": FormatterView(XmlFormatter()),
            },
            "hash-generator": {
                "title": "Hash",
                "category": "generator",
                "icon-name": "hash-symbolic",
                "tooltip": _("Calculate MD5, SHA1, SHA256 and SHA512 hashes and check for integrity"),
                "child": HashGeneratorView(),
            },
            "lorem-generator": {
                "title": "Lorem Ipsum",
                "category": "generator",
                "icon-name": "newspaper-symbolic",
                "tooltip": _("Generate lorem ipsum placeholder text"),
                "child": LoremGeneratorView(),
            },
            "uuid-generator": {
                "title": "UUID",
                "category": "generator",
                "icon-name": "fingerprint-symbolic",
                "tooltip": _("Generate Universally Unique IDs (UUID)"),
                "child": UuidGeneratorView(),
            },
            "text-inspector": {
                "title": "Inspector & Case Converter",
                "category": "text",
                "icon-name": "text-inspector-symbolic",
                "tooltip": _("View statistics about the typed text and change cases"),
                "child": TextInspectorView(),
            },
        }

        categories = {
            "converter": {
                "title": _("Converters"),
                "icon-name": "horizontal-arrows-symbolic",
                "child": TabContent(self._get_tools(tools, "converter"), "converter"),
            },
            "encoder": {
                "title": _("Encoders"),
                "icon-name": "encode-symbolic",
                "child": TabContent(self._get_tools(tools, "encoder"), "encoder"),
            },
            "formatter": {
                "title": _("Formatters"),
                "icon-name": "text-indent-symbolic",
                "child": TabContent(self._get_tools(tools, "formatter"), "formatter"),
            },
            "generator": {
                "title": _("Generators"),
                "icon-name": "plus-symbolic",
                "child": TabContent(self._get_tools(tools, "generator"), "generator"),
            },
            "text": {
                "title": _("Text"),
                "icon-name": "text-ab-symbolic",
                "child": TabContent(self._get_tools(tools, "text"), "text"),
            },
            "graphic": {
                "title": _("Graphics"),
                "icon-name": "brush-symbolic",
                "child": TabContent(self._get_tools(tools, "graphic"), "graphic"),
            },
        }

        # Setup tabs
        for c in categories:
            self._tabs_stack.add_named(categories[c]["child"], c)
            page = self._tabs_stack.get_page(categories[c]["child"])
            page.set_title(categories[c]["title"])
            page.set_icon_name(categories[c]["icon-name"])
            if c != "favorite":
                self._flap_btn.bind_property("active", page.get_child().get_flap(), "reveal-flap", GObject.BindingFlags.SYNC_CREATE)
                page.get_child().get_flap().bind_property("reveal-flap", self._flap_btn, "active", GObject.BindingFlags.SYNC_CREATE)

        # Restore last state
        self._settings.bind("window-width", self, "default-width", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-height", self, "default-height", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("sidebar-open", self._flap_btn, "active", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("last-tab", self._tabs_stack, "visible-child-name", Gio.SettingsBindFlags.DEFAULT)

        self.connect("close-request", self._on_close_request)

    def _on_close_request(self, data):
        content_stack = self._tabs_stack.get_visible_child().get_content_stack()
        self._settings.set_string("last-tool", content_stack.get_visible_child_name())

    def _on_flap_btn_clicked(self, data):
        self._flap.set_reveal_flap(self._flap_btn.get_active())

    def _get_tools(self, tools: dict, category: str):
        tools_in_category = {}
        for t in tools:
            if tools[t]["category"] == category:
                tools_in_category[t] = tools[t]
        return tools_in_category
