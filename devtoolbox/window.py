# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gettext import gettext as _
from gi.repository import Gtk, Adw, Gio
from devtoolbox.services.json_formatter import JsonFormatter
from devtoolbox.services.sql_formatter import SqlFormatter
from devtoolbox.services.xml_formatter import XmlFormatter
from devtoolbox.widgets.favorites_view import FavoritesView

from devtoolbox.widgets.utilities_view import UtilitiesView
from devtoolbox.views.base64_encoder_utility import Base64EncoderUtility
from devtoolbox.views.cron_parser_utility import CronParserUtility
from devtoolbox.views.formatter_utility import FormatterUtility
from devtoolbox.views.hash_generator_utility import HashGeneratorUtility
from devtoolbox.views.lorem_ipsum_utility import LoremIpsumGenerator, LoremIpsumUtility
from devtoolbox.views.jwt_decoder_utility import JWTDecoderUtility
from devtoolbox.views.gzip_encoder_utility import GZipEncoderUtility
from devtoolbox.views.html_encoder_utility import HtmlEncoderUtility
from devtoolbox.views.json2yaml_utility import Json2YamlUtility
from devtoolbox.views.number_base_utility import NumberBaseUtility
from devtoolbox.views.timestamp_utility import TimestampUtility
from devtoolbox.views.url_encoder_utility import UrlEncoderUtility


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/main.ui")
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    main_content = Gtk.Template.Child()
    tab_stack = Gtk.Template.Child()

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

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
                "child": NumberBaseUtility()
            },
            "cronparser": {
                "title": _("Cron Parser"),
                "icon-name": "hourglass-half-symbolic",
                "child": CronParserUtility()
            }
        }
        ENCODERS_UTILITIES = {
            "htmlencoder": {
                "title": _("HTML"),
                "icon-name": "code-symbolic",
                "child": HtmlEncoderUtility()
            },
            "urlencoder": {
                "title": _("URL"),
                "icon-name": "link-symbolic",
                "child": UrlEncoderUtility()
            },
            "base64encoder": {
                "title": _("Base64"),
                "icon-name": "base64-symbolic",
                "child": Base64EncoderUtility()
            },
            "gzipencoder": {
                "title": _("GZip"),
                "icon-name": "file-zip-symbolic",
                "child": GZipEncoderUtility()
            },
            "jwtdecoder": {
                "title": _("JWT"),
                "icon-name": "key-symbolic",
                "child": JWTDecoderUtility()
            }
        }
        FORMATTERS_UTILITIES = {
            "jsonformatter": {
                "title": "JSON",
                "icon-name": "right-left-symbolic",
                "child": FormatterUtility(JsonFormatter())
            },
            "sqlformatter": {
                "title": "SQL",
                "icon-name": "db-symbolic",
                "child": FormatterUtility(SqlFormatter())
            },
            "xmlformatter": {
                "title": "XML",
                "icon-name": "code-symbolic",
                "child": FormatterUtility(XmlFormatter())
            }
        }
        GENERATORS_UTILITIES = {
            "hashgen": {
                "title": "Hash Generator",
                "icon-name": "hashtag-symbolic",
                "child": HashGeneratorUtility()
            },
            "loremipsum": {
                "title": "Lorem Ipsum",
                "icon-name": "paragraph-symbolic",
                "child": LoremIpsumUtility()
            },
        }
        TABS = {
            "favorites": {
                "title": _("Favorites"),
                "icon-name": "starred",
                "child": FavoritesView()
            },
            "converters": {
                "title": _("Converters"),
                "icon-name": "right-left-symbolic",
                "child": UtilitiesView(CONVERTERS_UTILITIES)
            },
            "encoders": {
                "title": _("Encoders"),
                "icon-name": "folder-templates-symbolic",
                "child": UtilitiesView(ENCODERS_UTILITIES)
            },
            "formatters": {
                "title": _("Formatters"),
                "icon-name": "text-indent-more-symbolic",
                "child": UtilitiesView(FORMATTERS_UTILITIES)
            },
            "generators": {
                "title": _("Generators"),
                "icon-name": "plus-symbolic",
                "child": UtilitiesView(GENERATORS_UTILITIES)
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

        # Restore last state
        # Tab
        self.tab_stack.set_visible_child_name(
            self.settings.get_string("last-tab"))

        # Utility, favorites start always with first utility
        if self.tab_stack.get_visible_child_name() != "favorites":
            self.tab_stack.get_visible_child().sidebar_stack.set_visible_child_name(
                self.settings.get_string("last-utility"))
            for i in range(0, 10):
                    row = self.tab_stack.get_visible_child().sidebar.get_row_at_index(i)
                    if row != None and row.get_page_name() == self.settings.get_string("last-utility"):
                        self.tab_stack.get_visible_child().sidebar.select_row(row)

        # Window size
        self.settings.bind("window-width", self, "default-width",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("window-height", self, "default-height",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("window-maximized", self, "maximized",
                           Gio.SettingsBindFlags.DEFAULT)

        # Signals
        self.connect("close-request", self.on_close_request)

    def on_close_request(self, data):
        tab = self.tab_stack.get_visible_child_name()
        if tab != "favorites":
            utility = self.tab_stack.get_visible_child().sidebar_stack.get_visible_child_name()
            self.settings.set_string("last-utility", utility)
        self.settings.set_string("last-tab", tab)