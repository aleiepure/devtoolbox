# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GLib
from gettext import gettext as _, pgettext as C_

from .widgets.sidebar_item import SidebarItem
from .widgets.theme_switcher import ThemeSwitcher

from .views.json_yaml import JsonYamlView
from .views.timestamp import TimestampView
from .views.base_converter import BaseConverterView
from .views.cron_converter import CronConverterView
from .views.html_encoder import HtmlEncoderView
from .views.base64_encoder import Base64EncoderView
from .views.url_encoder import UrlEncoderView
from .views.gzip_compressor import GzipCompressorView
from .views.jwt_decoder import JwtDecoderView
from .views.formatter import FormatterView
from .views.hash_generator import HashGeneratorView
from .views.lorem_generator import LoremGeneratorView
from .views.uuid_generator import UuidGeneratorView
from .views.text_inspector import TextInspectorView
from .views.regex_tester import RegexTesterView
from .views.text_diff import TextDiffView
from .views.xml_validator import XmlValidatorView
from .views.markdown_preview import MarkdownPreviewView
from .views.color_converter import ColorConverterView
from .views.contrast_checker import ContrastCheckerView
from .views.colorblindness_simulator import ColorblindnessSimulatorView
from .views.image_converter import ImageConverterView
from .views.certificate_parser import CertificateParserView
from .views.random_generator import RandomGeneratorView
from .views.certificate_request_generator import CertificateRequestGeneratorView
from .views.reverse_cron import ReverseCronView
from .views.chmod_calculator import ChmodCalculatorView
from .views.qrcode_generator import QRCodeGeneratorView
from .views.json_validator import JsonValidatorView

from .formatters.json import JsonFormatter
from .formatters.sql import SqlFormatter
from .formatters.xml import XmlFormatter
from .formatters.html import HtmlFormatter
from .formatters.js import JsFormatter
from .formatters.css import CssFormatter

from .formatters.css_minifier import CssMinifier
from .formatters.js_minifier import JsMinifier


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/window.ui")
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = "DevtoolboxWindow"

    # Template elements
    _split_view = Gtk.Template.Child()
    _show_search_btn = Gtk.Template.Child()
    _search_bar = Gtk.Template.Child()
    _search_entry = Gtk.Template.Child()
    _fav_btn = Gtk.Template.Child()
    _fav_stack = Gtk.Template.Child()
    _favorites = Gtk.Template.Child()
    _sidebar = Gtk.Template.Child()
    _toggle_sidebar_btn = Gtk.Template.Child()
    _show_sidebar_btn = Gtk.Template.Child()
    _menu_btn = Gtk.Template.Child()
    _content_stack = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def _toggle_search(self, new_state: GLib.Variant, source: Gtk.Widget) -> None:
        """
        Callback for the win.search action

        Args:
            new_state (bool): new selected state
            source (Gtk.Widget): widget that caused the activation

        Returns:
            None
        """

        source._search_bar.set_search_mode(new_state.get_boolean())
        source._show_search_btn.set_active(new_state.get_boolean())
        self.set_state(new_state)

    def _refresh_favorites(self, new_state: None, source: Gtk.Widget) -> None:
        """
        Callback for the win.search action

        Args:
            new_state (None): stateless action, always None
            source (Gtk.Widget): widget that caused the activation

        Returns:
            None
        """

        source._populate_favorites()

    _actions = {
        ('search', None, None, 'false', _toggle_search),
        ('refresh-favorites', _refresh_favorites)
    }

    def __init__(self, debug, **kwargs):
        super().__init__(**kwargs)

        self.add_action_entries(self._actions, self)

        # Theme (Adapted from https://gitlab.gnome.org/tijder/blueprintgtk/)
        self._menu_btn.get_popover().add_child(ThemeSwitcher(), "themeswitcher")
        if debug == "False":
            self.remove_css_class("devel")

        self._tools = {

            # Converters
            "json-yaml": {
                "title": "JSON - YAML",
                "category": _("Converters"),
                "icon-name": "horizontal-arrows-symbolic",
                "tooltip": _("Convert JSON documents to YAML and vice-versa"),
                "child": JsonYamlView(),
                "keywords": [
                    "json",
                    "yaml",
                    "yml",
                    C_("search keyword", "parse"),
                    C_("search keyword", "converter"),
                    C_("search keyword", "convert"),
                    C_("search keyword", "format"),
                    C_("search keyword", "document"),
                    C_("search keyword", "spaces"),
                    C_("search keyword", "indentation"),
                    C_("search keyword", "indent")
                ]
            },
            "timestamp": {
                "title": _("Timestamp"),
                "category": _("Converters"),
                "icon-name": "calendar-symbolic",
                "tooltip": _("Convert UNIX timestamps to and from plain dates"),
                "child": TimestampView(),
                "keywords": [
                    C_("search keyword", "epoch"),
                    C_("search keyword", "time"),
                    C_("search keyword", "format"),
                    C_("search keyword", "parse"),
                    C_("search keyword", "datetime"),
                    C_("search keyword", "calendar"),
                    C_("search keyword", "timestamp"),
                    "unix",
                    C_("search keyword", "date"),
                    C_("search keyword", "converter"),
                    C_("search keyword", "convert"),
                    C_("search keyword", "format"),
                    C_("search keyword", "short"),
                    C_("search keyword", "long"),
                    "ISO",
                    "RFC",
                    C_("search keyword", "year"),
                    C_("search keyword", "month"),
                    C_("search keyword", "day"),
                    C_("search keyword", "hour"),
                    C_("search keyword", "hours"),
                    C_("search keyword", "minute"),
                    C_("search keyword", "minutes"),
                    C_("search keyword", "second"),
                    C_("search keyword", "seconds"),
                    C_("search keyword", "timezone"),
                    C_("search keyword", "now"),
                ]
            },
            "base-converter": {
                "title": _("Number Bases"),
                "category": _("Converters"),
                "icon-name": "hashtag-symbolic",
                "tooltip": _("Convert numbers between bases"),
                "child": BaseConverterView(),
                "keywords": [
                    C_("search keyword", "representation"),
                    C_("search keyword", "base"),
                    C_("search keyword", "converter"),
                    C_("search keyword", "convert"),
                    C_("search keyword", "number"),
                    C_("search keyword", "binary"),
                    C_("search keyword", "octal"),
                    C_("search keyword", "decimal"),
                    C_("search keyword", "hexadecimal"),
                    C_("search keyword", "integer"),
                    "ascii",
                    "utf-8",
                    "utf8"
                ]
            },
            "cron": {
                "title": _("CRON Parser"),
                "category": _("Converters"),
                "icon-name": "timer-symbolic",
                "tooltip": _("Convert CRON expressions to time and date"),
                "child": CronConverterView(),
                "keywords": [
                    "cron",
                    C_("search keyword", "schedule"),
                    C_("search keyword", "parser"),
                    C_("search keyword", "expression"),
                    C_("search keyword", "convert"),
                    C_("search keyword", "time"),
                    C_("search keyword", "date"),
                    C_("search keyword", "job"),
                    "linux",
                    "unix",
                ]
            },
            "reverse-cron": {
                "title": _("Reverse CRON"),
                "category": _("Converters"),
                "icon-name": "timer-reverse-symbolic",
                "tooltip": _("Generate CRON expressions"),
                "child": ReverseCronView(),
                "keywords": [
                    "cron",
                    C_("search keyword", "schedule"),
                    C_("search keyword", "parser"),
                    C_("search keyword", "expression"),
                    C_("search keyword", "convert"),
                    C_("search keyword", "time"),
                    C_("search keyword", "date"),
                    C_("search keyword", "job"),
                    "linux",
                    "unix",
                ]
            },

            # Encoders
            "html-encoder": {
                "title": "HTML",
                "category": _("Encoders & Decoders"),
                "icon-name": "code-symbolic",
                "tooltip": _("Encode and decode special characters using the HTML format"),
                "child": HtmlEncoderView(),
                "keywords": [
                    "html",
                    C_("search keyword", "escape"),
                    "web",
                    C_("search keyword", "markup"),
                    C_("search keyword", "text"),
                ]
            },
            "base64-encoder": {
                "title": "Base64",
                "category": _("Encoders & Decoders"),
                "icon-name": "base64-symbolic",
                "tooltip": _("Encode and decode base64 strings"),
                "child": Base64EncoderView(),
                "keywords": [
                    "base64",
                    C_("search keyword", "string"),
                    C_("search keyword", "text"),
                    C_("search keyword", "data"),
                ]
            },
            "url-encoder": {
                "title": "URL",
                "category": _("Encoders & Decoders"),
                "icon-name": "chain-link-symbolic",
                "tooltip": _("Encode and decode special characters inside URLs"),
                "child": UrlEncoderView(),
                "keywords": [
                    C_("search keyword", "url"),
                    C_("search keyword", "unescape"),
                    C_("search keyword", "web"),
                    C_("search keyword", "link"),
                    C_("search keyword", "address"),
                    C_("search keyword", "uri"),
                    C_("search keyword", "query"),
                ]
            },
            "gzip-compressor": {
                "title": "GZip",
                "category": _("Encoders & Decoders"),
                "icon-name": "shoe-box-symbolic",
                "tooltip": _("Compress and decompress files and texts using GZip"),
                "child": GzipCompressorView(),
                "keywords": [
                    C_("search keyword", "unarchive"),
                    C_("search keyword", "file"),
                    C_("search keyword", "text"),
                    C_("search keyword", "string"),
                    C_("search keyword", "zip"),
                    C_("search keyword", "unzip"),
                    C_("search keyword", "decompression"),
                    C_("search keyword", "decompressor")
                ]
            },
            "jwt-decoder": {
                "title": "JWT",
                "category": _("Encoders & Decoders"),
                "icon-name": "key-symbolic",
                "tooltip": _("Decode JWT tokens to header and payload"),
                "child": JwtDecoderView(),
                "keywords": [
                    C_("search keyword", "json web token"),
                    C_("search keyword", "header"),
                    C_("search keyword", "payload"),
                    C_("search keyword", "signature"),
                    C_("search keyword", "authentication"),
                    C_("search keyword", "authorization"),
                    C_("search keyword", "security"),
                ]
            },

            # Formatters and minifiers
            "json-formatter": {
                "title": "JSON",
                "category": _("Formatters & Minifiers"),
                "icon-name": "json-symbolic",
                "tooltip": _("Format JSON documents"),
                "child": FormatterView(JsonFormatter()),
                "keywords": [
                    C_("search keyword", "pretty"),
                    C_("search keyword", "indent"),
                    C_("search keyword", "beautify"),
                    C_("search keyword", "parse"),
                    C_("search keyword", "data"),
                ]
            },
            "sql-formatter": {
                "title": "SQL",
                "category": _("Formatters & Minifiers"),
                "icon-name": "database-symbolic",
                "tooltip": _("Format SQL documents"),
                "child": FormatterView(SqlFormatter()),
                "keywords": [
                    C_("search keyword", "pretty"),
                    C_("search keyword", "indent"),
                    C_("search keyword", "beautify"),
                    C_("search keyword", "query"),
                    C_("search keyword", "database"),
                    C_("search keyword", "statement"),
                ]
            },
            "xml-formatter": {
                "title": "XML",
                "category": _("Formatters & Minifiers"),
                "icon-name": "code-symbolic",
                "tooltip": _("Format XML documents"),
                "child": FormatterView(XmlFormatter()),
                "keywords": [
                    C_("search keyword", "pretty"),
                    C_("search keyword", "indent"),
                    C_("search keyword", "beautify"),
                    C_("search keyword", "markup"),
                    C_("search keyword", "document"),
                    C_("search keyword", "data"),
                ]
            },
            "html-formatter": {
                "title": "HTML",
                "category": _("Formatters & Minifiers"),
                "icon-name": "html-symbolic",
                "tooltip": _("Format HTML documents"),
                "child": FormatterView(HtmlFormatter()),
                "keywords": [
                    C_("search keyword", "pretty"),
                    C_("search keyword", "indent"),
                    C_("search keyword", "beautify"),
                    C_("search keyword", "markup"),
                    C_("search keyword", "minify"),
                    C_("search keyword", "web"),
                    C_("search keyword", "document"),
                ]
            },
            "js-formatter": {
                "title": "JavaScript",
                "category": _("Formatters & Minifiers"),
                "icon-name": "js-symbolic",
                "tooltip": _("Format JavaScript documents"),
                "child": FormatterView(JsFormatter()),
                "keywords": [
                    "js",
                    C_("search keyword", "pretty"),
                    C_("search keyword", "indent"),
                    C_("search keyword", "beautify"),
                    C_("search keyword", "minify"),
                    C_("search keyword", "code"),
                ]
            },
            "css-formatter": {
                "title": "CSS",
                "category": _("Formatters & Minifiers"),
                "icon-name": "css-symbolic",
                "tooltip": _("Format CSS documents"),
                "child": FormatterView(CssFormatter()),
                "keywords": [
                    C_("search keyword", "pretty"),
                    C_("search keyword", "indent"),
                    C_("search keyword", "beautify"),
                    C_("search keyword", "minify"),
                    C_("search keyword", "stylesheet"),
                ]
            },
            "css-minifier": {
                "title": _("CSS Minifier"),
                "category": _("Formatters & Minifiers"),
                "icon-name": "css-symbolic",
                "tooltip": _("Minify CSS documents"),
                "child": FormatterView(CssMinifier()),
                "keywords": [
                    C_("search keyword", "minify"),
                    C_("search keyword", "compress"),
                    C_("search keyword", "style"),
                    C_("search keyword", "stylesheet"),
                    C_("search keyword", "reduce"),
                    C_("search keyword", "size"),
                ]
            },
            "js-minifier": {
                "title": _("JavaScript Minifier"),
                "category": _("Formatters & Minifiers"),
                "icon-name": "js-symbolic",
                "tooltip": _("Minify JavaScript documents"),
                "child": FormatterView(JsMinifier()),
                "keywords": [
                    "js",
                    C_("search keyword", "minify"),
                    C_("search keyword", "compress"),
                    C_("search keyword", "reduce"),
                    C_("search keyword", "size"),
                    C_("search keyword", "script"),
                    C_("search keyword", "code"),
                ]
            },

            # Generators
            "hash-generator": {
                "title": _("Hash"),
                "category": _("Generators"),
                "icon-name": "hash-symbolic",
                "tooltip": _("Calculate MD5, SHA1, SHA256, and SHA512 hashes and check for integrity"),
                "child": HashGeneratorView(),
                "keywords": [
                    C_("search keyword", "checksum"),
                    C_("search keyword", "digest"),
                    C_("search keyword", "generate"),
                    C_("search keyword", "security"),
                    C_("search keyword", "cryptography"),
                ]
            },
            "lorem-generator": {
                "title": "Lorem Ipsum",
                "category": _("Generators"),
                "icon-name": "newspaper-symbolic",
                "tooltip": _("Generate lorem ipsum placeholder text"),
                "child": LoremGeneratorView(),
                "keywords": [
                    C_("search keyword", "dummy"),
                    C_("search keyword", "sample"),
                    C_("search keyword", "filler"),
                    C_("search keyword", "latin"),
                ]
            },
            "uuid-generator": {
                "title": "UUID",
                "category": _("Generators"),
                "icon-name": "fingerprint-symbolic",
                "tooltip": _("Generate Universally Unique IDs (UUID)"),
                "child": UuidGeneratorView(),
                "keywords": [
                    "guid",
                    C_("search keyword", "identifier"),
                    C_("search keyword", "random"),
                ]
            },
            "random-generator": {
                "title": _("Random"),
                "category": _("Generators"),
                "icon-name": "dice3-symbolic",
                "tooltip": _("Generate random numbers and strings"),
                "child": RandomGeneratorView(),
                "keywords": [
                    C_("search keyword", "password"),
                    C_("search keyword", "token"),
                    C_("search keyword", "entropy"),
                    C_("search keyword", "secure"),
                ]
            },
            "chmod": {
                "title": _("Chmod Calculator"),
                "category": _("Generators"),
                "icon-name": "general-properties-symbolic",
                "tooltip": _("Calculate values to modify permissions with chmod"),
                "child": ChmodCalculatorView(),
                "keywords": [
                    C_("search keyword", "file"),
                    C_("search keyword", "unix"),
                    C_("search keyword", "linux"),
                    C_("search keyword", "calculate"),
                    C_("search keyword", "mode"),
                    C_("search keyword", "access"),
                ]
            },
            "qrcode": {
                "title": _("QR Code"),
                "category": _("Generators"),
                "icon-name": "qr-code-symbolic",
                "tooltip": _("Create custom QR Codes"),
                "child": QRCodeGeneratorView(),
                "keywords": [
                    C_("search keyword", "qrcode"),
                    C_("search keyword", "barcode"),
                    C_("search keyword", "image"),
                    C_("search keyword", "matrix"),
                ]
            },

            # Text
            "text-inspector": {
                "title": _("Text Inspector & Case Converter"),
                "category": _("Text"),
                "icon-name": "text-inspector-symbolic",
                "tooltip": _("View statistics about text and change sentence cases"),
                "child": TextInspectorView(),
                "keywords": [
                    C_("search keyword", "analyze"),
                    C_("search keyword", "convert"),
                    C_("search keyword", "uppercase"),
                    C_("search keyword", "lowercase"),
                    C_("search keyword", "capitalize"),
                    C_("search keyword", "count"),
                    C_("search keyword", "words"),
                    C_("search keyword", "characters"),
                    C_("search keyword", "lines"),
                ]
            },
            "regex-tester": {
                "title": _("Regex Tester"),
                "category": _("Text"),
                "icon-name": "regex-symbolic",
                "tooltip": _("Find matching strings inside a text"),
                "child": RegexTesterView(),
                "keywords": [
                    C_("search keyword", "expression"),
                    C_("search keyword", "pattern"),
                    C_("search keyword", "search"),
                ]
            },
            "text-diff": {
                "title": _("Text Diff"),
                "category": _("Text"),
                "icon-name": "open-book-symbolic",
                "tooltip": _("Analyze two texts and find differences"),
                "child": TextDiffView(),
                "keywords": [
                    C_("search keyword", "difference"),
                    C_("search keyword", "compare"),
                    C_("search keyword", "changes"),
                    C_("search keyword", "modification"),
                ]
            },
            "xml-validator": {
                "title": _("XML Scheme Validator"),
                "category": _("Text"),
                "icon-name": "xml-check-symbolic",
                "tooltip": _("Check an XML file against an XSD schema"),
                "child": XmlValidatorView(),
                "keywords": [
                    C_("search keyword", "validate"),
                    C_("search keyword", "markup"),
                    C_("search keyword", "document"),
                ]
            },
            "json-validator": {
                "title": _("JSON Schema Validator"),
                "category": _("Text"),
                "icon-name": "json-check-symbolic",
                "tooltip": _("Check a JSON file against a JSON schema"),
                "child": JsonValidatorView(),
                "keywords": [
                    C_("search keyword", "validate"),
                    C_("search keyword", "data"),
                    C_("search keyword", "document"),
                ]
            },
            "markdown-preview": {
                "title": _("Markdown Previewer"),
                "category": _("Text"),
                "icon-name": "markdown-symbolic",
                "tooltip": _("Preview markdown code as you type"),
                "child": MarkdownPreviewView(),
                "keywords": [
                    C_("search keyword", "render"),
                    C_("search keyword", "markup"),
                    C_("search keyword", "md"),
                ]
            },

            # Graphics
            "color-converter": {
                "title": _("Color Converter"),
                "category": _("Graphics"),
                "icon-name": "color-symbolic",
                "tooltip": _("Convert colors between formats"),
                "child": ColorConverterView(),
            },
            "contrast-checker": {
                "title": _("Contrast Checker"),
                "category": _("Graphics"),
                "icon-name": "image-adjust-contrast-symbolic",
                "tooltip": _("Check a color combination for WCAG compliance"),
                "child": ContrastCheckerView(),
                "keywords": [
                    C_("search keyword", "accessibility"),
                    C_("search keyword", "ratio"),
                ]
            },
            "colorblind-sim": {
                "title": _("Color Blindness"),
                "category": _("Graphics"),
                "icon-name": "eye-open-symbolic",
                "tooltip": _("Simulate color blindness in images"),
                "child": ColorblindnessSimulatorView(),
                "keywords": [
                    C_("search keyword", "simulation"),
                    C_("search keyword", "daltonism"),
                    C_("search keyword", "protanopia"),
                    C_("search keyword", "deuteranopia"),
                    C_("search keyword", "tritanopia"),
                    C_("search keyword", "vision"),
                ]
            },
            "image-converter": {
                "title": _("Image Format Converter"),
                "category": _("Graphics"),
                "icon-name": "image-symbolic",
                "tooltip": _("Convert images to different formats"),
                "child": ImageConverterView(),
                "keywords": [
                "image",
                    C_("search keyword", "jpg"),
                    C_("search keyword", "jpeg"),
                    C_("search keyword", "png"),
                    C_("search keyword", "bmp"),
                    C_("search keyword", "gif"),
                    C_("search keyword", "webp"),
                    C_("search keyword", "picture"),
                ]
            },

            # Certificates
            "certificate-parser": {
                "title": _("Certificate Parser"),
                "category": _("Certificates"),
                "icon-name": "certificate-parser-symbolic",
                "tooltip": _("View certificates contents"),
                "child": CertificateParserView(),
                "keywords": [
                    "x509",
                    "pem",
                    "crt",
                    "ssl",
                    "tls",
                    C_("search keyword", "key"),
                    C_("search keyword", "security"),
                    C_("search keyword", "public key"),
                    C_("search keyword", "cryptography"),
                ]
            },
            "csr-generator": {
                "title": _("Certificate Signing Request"),
                "category": _("Certificates"),
                "icon-name": "csr-symbolic",
                "tooltip": _("Generate certificate signing requests"),
                "child": CertificateRequestGeneratorView(),
                "keywords": [
                    "csr",
                    "ssl",
                    "tls",
                    "x509",
                    "pem",
                    C_("search keyword", "key"),
                    C_("search keyword", "security"),
                    C_("search keyword", "cryptography"),
                ]
            },
        }

        # Populate sidebar and content stack
        for t in self._tools:
            self._sidebar.append(SidebarItem(
                tool_name=t,
                title=self._tools[t]["title"],
                icon_name=self._tools[t]["icon-name"],
                tool_tip=self._tools[t]["tooltip"],
                category=self._tools[t]["category"]))
            self._content_stack.add_named(self._tools[t]["child"], t)

            self._sidebar.set_header_func(
                self._create_sidebar_headers, None, None)
            self._sidebar.set_filter_func(self._filter_func, None, None)

            # Populate favorites
            self._populate_favorites()
            if self._favorites.get_row_at_index(0) is not None:
                self._fav_stack.set_visible_child_name("filled")

            # Select row for visible content
            try:
                index = list(self._tools.keys()).index(
               self._settings.get_string("last-tool"))
                if index == 0:
                    self._sidebar.select_row(self._sidebar.get_first_child())
                else:
                    self._sidebar.select_row(
                        self._sidebar.get_row_at_index(index))
            except ValueError:
                self._sidebar.select_row(self._sidebar.get_first_child())

                # Restore last state
                self._settings.bind("window-width", self,
                    "default-width", Gio.SettingsBindFlags.DEFAULT)
                self._settings.bind("window-height", self,
                    "default-height", Gio.SettingsBindFlags.DEFAULT)
                self._settings.bind("window-maximized", self,
                    "maximized", Gio.SettingsBindFlags.DEFAULT)
                self._settings.bind("sidebar-open", self._toggle_sidebar_btn,
                    "active", Gio.SettingsBindFlags.DEFAULT)
                self._settings.bind("last-tool", self._content_stack,
                    "visible-child-name", Gio.SettingsBindFlags.DEFAULT)

    @Gtk.Template.Callback()
    def _on_favorite_row_activated(self, list_box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        """
        Callback for "row-activated" signal.
        Changes visible view and the selected row in the sidebar, closes the popover and the sidebar if the window is too small.

        Args:
            list_box (Gtk.ListBox): ListBox interracted with
            row (Gtk.ListBoxRow): selected row in ListBox

        Returns:
            None
        """

        self._content_stack.set_visible_child_name(row.get_tool_name())

        idx = 0
        sidebar_row = self._sidebar.get_row_at_index(idx)
        while sidebar_row is not None:
            if row.get_tool_name() == sidebar_row.get_tool_name():
                self._sidebar.select_row(sidebar_row)
                self._sidebar.grab_focus()
                break
            idx += 1
            sidebar_row = self._sidebar.get_row_at_index(idx)

        self._fav_btn.popdown()
        if not self._toggle_sidebar_btn.get_visible():
            self._split_view.set_show_sidebar(False)

    @Gtk.Template.Callback()
    def _on_sidebar_row_activated(self, list_box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        """
        Callback for "row-activated" signal.
        Changes visible view and closes sidebar if the window is too small.

        Args:
            list_box (Gtk.ListBox): ListBox interracted with
            row (Gtk.ListBoxRow): selected row in ListBox

        Returns:
            None
        """

        self._content_stack.set_visible_child_name(row.get_tool_name())

        # Toggle not visible? => sidebar over content, close on selection
        if not self._toggle_sidebar_btn.get_visible():
            self._split_view.set_show_sidebar(False)

    @Gtk.Template.Callback()
    def _on_map(self, user_data: object | None) -> None:
        """
        Callback for "map" signal.
        Grab sidebar focus to move scrolled window where the selected row is visible and immediately change focus to the
        tool in use.

        Args:
            user_data (object or None): additional data passed to the callback

        Returns:
            None
        """

        self._sidebar.grab_focus()
        self._content_stack.get_visible_child().grab_focus()

    @Gtk.Template.Callback()
    def _on_sidebar_btn_clicked(self, user_data: object | None) -> None:
        """
        Callback for "clicked" signal.
        Shows the sidebar.

        Args:
            user_data (object or None): additional data passed to the callback

        Returns:
            None
        """

        self._split_view.set_show_sidebar(True)

    def _create_sidebar_headers(self, row: Gtk.ListBoxRow, before: Gtk.ListBoxRow, user_data: object | None, dummy: None) -> None:
        """
        Creates the sidebar headers to separate the categories. Loops on every sidebar item.

        Args:
            row (Gtk.ListBoxRow): list box analyzed
            before (Gtk.ListBoxRow): list box preceding `row`
            user_data (object or None): additional data passed to the callback
            dummy (None): required variable to make function work (why?)

        Returns:
            None
        """

        if before is None or before.get_category() != row.get_category():
            header_label= Gtk.Label(label=row.get_category())
            header_label.set_halign(Gtk.Align.START)
            header_label.set_valign(Gtk.Align.CENTER)
            header_label.add_css_class("heading")
            header_label.add_css_class("dimmed")
            header_label.set_margin_start(12)
            header_label.set_margin_bottom(6)

            if before:
                header_label.set_margin_top(16)

            row.set_header(header_label)

    @ Gtk.Template.Callback()
    def _on_searchentry_search_changed(self, user_data: object | None) -> None:
        """
        Callback for "search-changed" signal.
        Invalidates filter to perform search.

        user_data (object or None): additional data passed to the callback
            dummy (None): required variable to make function work (why?)

        Returns:
            None
        """

        self._sidebar.invalidate_filter()

    def _filter_func(self, row: Gtk.ListBoxRow, user_data: object | None, dummy: None) -> bool:
        """
        Loops on every sidebar item and returns True if the title or tooltip
        contain the searched text.

        Args:
            row (Gtk.ListBoxRow): list box analyzed
            user_data (object or None): additional data passed to the callback
            dummy (None): required variable to make function work (why?)

        Returns:
            bool with the result
        """

        search_query= self._search_entry.get_text().lower()
        if not search_query:
            return True

        tool_name= row.get_tool_name()
        tool_data= self._tools.get(tool_name, {})

        title= row.get_title().lower()
        tooltip= row.get_tool_tip().lower()
        category= row.get_category().lower()
        keywords= " ".join(tool_data.get("keywords", [])).lower()

        if (
            search_query in title or
            search_query in tooltip or
            search_query in category or
            search_query in keywords
        ):
            return True

        return False

    def _populate_favorites(self) -> None:
        """
        Populates the favorites popover with the currrent gsettings values.

        Args:
            None

        Returns:
            None
        """

        self._favorites.remove_all()

        favorite_tools= self._settings.get_strv('favorites')
        if len(favorite_tools) == 0:
            self._fav_stack.set_visible_child_name('empty')
        else:
            self._fav_stack.set_visible_child_name('filled')
            for t in self._tools:
                if t in favorite_tools:
                    self._favorites.append(
                                SidebarItem(
                                        tool_name=t,
                                        title=self._tools[t]["title"],
                                        icon_name=self._tools[t]["icon-name"],
                                        tool_tip=self._tools[t]["tooltip"],
                                        category=self._tools[t]["category"]
                                    )
                                )
