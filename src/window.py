# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GObject
from gettext import gettext as _

from .widgets.sidebar_item import SidebarItem
from .widgets.theme_switcher import ThemeSwitcher

from .views.tab_content import TabContent
from .views.json_yaml import JsonYamlView
from .views.timestamp import TimestampView
from .views.base_converter import BaseConverterView
from .views.cron_converter import CronConverterView
from .views.html_encoder import HtmlEncoderView
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
from .views.contrast_checker import ContrastCheckerView
from .views.colorblindness_simulator import ColorblindnessSimulatorView
from .views.image_converter import ImageConverterView
from .views.certificate_parser import CertificateParserView
from .views.random_generator import RandomGeneratorView
from .views.certificate_request_generator import CertificateRequestGeneratorView
from .views.reverse_cron import ReverseCronView
from .views.chmod_calculator import ChmodCalculatorView
from .views.qrcode_generator import QRCodeGeneratorView

from .formatters.json import JsonFormatter
from .formatters.sql import SqlFormatter
from .formatters.xml import XmlFormatter
from .formatters.html import HtmlFormatter
from .formatters.js import JsFormatter


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/window.ui")
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = "DevtoolboxWindow"

    # Template elements
    _title = Gtk.Template.Child()
    _flap_btn = Gtk.Template.Child()
    _tabs_stack = Gtk.Template.Child()
    _menu_btn = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, debug, **kwargs):
        super().__init__(**kwargs)

        # Theme (Adapted from https://gitlab.gnome.org/tijder/blueprintgtk/)
        self._menu_btn.get_popover().add_child(ThemeSwitcher(), "themeswitcher");
        if debug == "False":
            self.remove_css_class("devel")

        tools = {
            "json-yaml": {
                "title": "JSON - YAML",
                "category": "converter",
                "icon-name": "horizontal-arrows-symbolic",
                "tooltip": _("Convert JSON documents to YAML and vice-versa"),
                "child": JsonYamlView(),
            },
            "timestamp": {
                "title": _("Timestamp"),
                "category": "converter",
                "icon-name": "calendar-symbolic",
                "tooltip": _("Convert UNIX timestamps to and from plain dates"),
                "child": TimestampView(),
            },
            "base-converter": {
                "title": _("Number Bases"),
                "category": "converter",
                "icon-name": "hashtag-symbolic",
                "tooltip": _("Convert numbers between bases"),
                "child": BaseConverterView(),
            },
            "cron": {
                "title": _("CRON Parser"),
                "category": "converter",
                "icon-name": "timer-symbolic",
                "tooltip": _("Convert CRON expressions to time and date"),
                "child": CronConverterView(),
            },
            "html-encoder": {
                "title": "HTML",
                "category": "encoder",
                "icon-name": "code-symbolic",
                "tooltip": _("Encode and decode special characters using the HTML format"),
                "child": HtmlEncoderView(),
            },
            "url-encoder": {
                "title": "URL",
                "category": "encoder",
                "icon-name": "chain-link-symbolic",
                "tooltip": _("Encode and decode special characters inside URLs"),
                "child": UrlEncoderView(),
            },
            "gzip-compressor": {
                "title": "GZip",
                "category": "encoder",
                "icon-name": "shoe-box-symbolic",
                "tooltip": _("Compress and decompress files and texts using GZip"),
                "child": GzipCompressorView(),
            },
            "jwt-decoder": {
                "title": "JWT",
                "category": "encoder",
                "icon-name": "key-symbolic",
                "tooltip": _("Decode JWT tokens to header and payload"),
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
                "tooltip": _("Calculate MD5, SHA1, SHA256, and SHA512 hashes and check for integrity"),
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
                "title": _("Text Inspector & Case Converter"),
                "category": "text",
                "icon-name": "text-inspector-symbolic",
                "tooltip": _("View statistics about text and change sentence cases"),
                "child": TextInspectorView(),
            },
            "regex-tester": {
                "title": _("Regex Tester"),
                "category": "text",
                "icon-name": "regex-symbolic",
                "tooltip": _("Find matching strings inside a text"),
                "child": RegexTesterView(),
            },
            "text-diff": {
                "title": _("Text Diff"),
                "category": "text",
                "icon-name": "open-book-symbolic",
                "tooltip": _("Analyze two texts and find differences"),
                "child": TextDiffView(),
            },
            "xml-validator": {
                "title": _("XML Scheme Validator"),
                "category": "text",
                "icon-name": "xml-check-symbolic",
                "tooltip": _("Check an XML file against an XSD schema"),
                "child": XmlValidatorView(),
            },
            "markdown-preview": {
                "title": _("Markdown Previewer"),
                "category": "text",
                "icon-name": "markdown-symbolic",
                "tooltip": _("Preview markdown code as you type"),
                "child": MarkdownPreviewView(),
            },
            "contrast-checker": {
                "title": _("Contrast Checker"),
                "category": "graphic",
                "icon-name": "image-adjust-contrast-symbolic",
                "tooltip": _("Check a color combination for WCAG compliance"),
                "child": ContrastCheckerView(),
            },
            "colorblind-sim": {
                "title": _("Color Blindness"),
                "category": "graphic",
                "icon-name": "color-symbolic",
                "tooltip": _("Simulate color blindness in images"),
                "child": ColorblindnessSimulatorView(),
            },
            "image-converter": {
                "title": _("Image Format Converter"),
                "category": "graphic",
                "icon-name": "image-symbolic",
                "tooltip": _("Convert images to different formats"),
                "child": ImageConverterView(),
            },
            "html-formatter": {
                "title": "HTML",
                "category": "formatter",
                "icon-name": "html-symbolic",
                "tooltip": _("Format HTML documents"),
                "child": FormatterView(HtmlFormatter()),
            },
            "certificate-parser": {
                "title": _("Certificate Parser"),
                "category": "encoder",
                "icon-name": "certificate-symbolic",
                "tooltip": _("View certificates contents"),
                "child": CertificateParserView(),
            },
             "random-generator": {
                "title": _("Random"),
                "category": "generator",
                "icon-name": "dice3-symbolic",
                "tooltip": _("Generate random numbers and strings"),
                "child": RandomGeneratorView(),
            },
            "csr-generator": {
                "title": _("Certificate Signing Request"),
                "category": "generator",
                "icon-name": "certificate-symbolic",
                "tooltip": _("Generate certificate signing requests"),
                "child": CertificateRequestGeneratorView(),
            },
            "reverse-cron": {
                "title": _("Reverse CRON"),
                "category": "converter",
                "icon-name": "timer-reverse-symbolic",
                "tooltip": _("Generate CRON expressions"),
                "child": ReverseCronView(),
            },
            "chmod": {
                "title": _("Chmod Calculator"),
                "category": "generator",
                "icon-name": "general-properties-symbolic",
                "tooltip": _("Calculate values to modify permissions with chmod"),
                "child": ChmodCalculatorView(),
            },
            "js-formatter": {
                "title": "JavaScript",
                "category": "formatter",
                "icon-name": "js-symbolic",
                "tooltip": _("Format JavaScript documents"),
                "child": FormatterView(JsFormatter()),
            },
            "qrcode": {
                "title": "QR Code",
                "category": "generator",
                "icon-name": "qr-code-symbolic",
                "tooltip": _("Create custom QR Codes"),
                "child": QRCodeGeneratorView(),
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

    def _on_close_request(self, user_data:GObject.GPointer):
        content_stack = self._tabs_stack.get_visible_child().get_content_stack()
        self._settings.set_string("last-tool", content_stack.get_visible_child_name())

    def _on_flap_btn_clicked(self, user_data:GObject.GPointer):
        self._flap.set_reveal_flap(self._flap_btn.get_active())

    def _get_tools(self, tools:dict, category:str):
        tools_in_category = {}
        for t in tools:
            if tools[t]["category"] == category:
                tools_in_category[t] = tools[t]
        return tools_in_category

    # def __update_style(self, style_manager, dark):
    #     if style_manager.get_dark():
    #         self._settings.set_string("style-scheme", "Adwaita-dark")
    #     else:
    #         self._settings.set_string("style-scheme", "Adwaita")
