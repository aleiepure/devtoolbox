# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gettext import gettext as _, pgettext as C_
from typing import List

# Tools metadata
TOOLS_METADATA = {
    # Converters
    "json-yaml": {
        "title": "JSON - YAML - TOML",
        "category": _("Converters"),
        "icon-name": "horizontal-arrows-symbolic",
        "tooltip": _("Convert between JSON, YAML, and TOML formats"),
        "keywords": [
            "json",
            "yaml",
            "yml",
            "toml",
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
        "tooltip": _("Decode and encode JWT tokens"),
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
        "tooltip": _("Calculate hashes and check for integrity"),
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
        "keywords": [
            C_("search keyword", "rgb"),
            C_("search keyword", "rgba"),
            C_("search keyword", "hex"),
            C_("search keyword", "hsl"),
            C_("search keyword", "hsv"),
            C_("search keyword", "cmyk"),
            C_("search keyword", "format"),
            C_("search keyword", "conversion"),
            C_("search keyword", "palette"),
        ]
    },
    "contrast-checker": {
        "title": _("Contrast Checker"),
        "category": _("Graphics"),
        "icon-name": "image-adjust-contrast-symbolic",
        "tooltip": _("Check a color combination for WCAG compliance"),
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

def get_tools_for_ui() -> dict:
    """
    Get tools configuration with UI components attached.
    Import view classes only when needed for UI.
    """
    
    tools_with_ui = {}
    for tool_id, config in TOOLS_METADATA.items():
        tools_with_ui[tool_id] = config.copy()

        match tool_id:
            
            # Converters
            case "json-yaml":
                from .views.json_yaml_toml import JsonYamlTomlView
                tools_with_ui[tool_id]["child"] = JsonYamlTomlView()
            case "timestamp":
                from .views.timestamp import TimestampView
                tools_with_ui[tool_id]["child"] = TimestampView()
            case "base-converter":
                from .views.base_converter import BaseConverterView
                tools_with_ui[tool_id]["child"] = BaseConverterView()
            case "cron":
                from .views.cron_converter import CronConverterView
                tools_with_ui[tool_id]["child"] = CronConverterView()
            case "reverse-cron":
                from .views.reverse_cron import ReverseCronView
                tools_with_ui[tool_id]["child"] = ReverseCronView()
            
            # Encoders
            case "html-encoder":
                from .views.html_encoder import HtmlEncoderView
                tools_with_ui[tool_id]["child"] = HtmlEncoderView()
            case "base64-encoder":
                from .views.base64_encoder import Base64EncoderView
                tools_with_ui[tool_id]["child"] = Base64EncoderView()
            case "url-encoder":
                from .views.url_encoder import UrlEncoderView
                tools_with_ui[tool_id]["child"] = UrlEncoderView()
            case "gzip-compressor":
                from .views.gzip_compressor import GzipCompressorView
                tools_with_ui[tool_id]["child"] = GzipCompressorView()
            case "jwt-decoder":
                from .views.jwt_decoder import JwtDecoderView
                tools_with_ui[tool_id]["child"] = JwtDecoderView()
            
            # Formatters and minifiers
            case "json-formatter":
                from .views.formatter import FormatterView
                from .formatters.json import JsonFormatter
                tools_with_ui[tool_id]["child"] = FormatterView(JsonFormatter())
            case "sql-formatter":
                from .views.formatter import FormatterView
                from .formatters.sql import SqlFormatter
                tools_with_ui[tool_id]["child"] = FormatterView(SqlFormatter())
            case "xml-formatter":
                from .views.formatter import FormatterView
                from .formatters.xml import XmlFormatter
                tools_with_ui[tool_id]["child"] = FormatterView(XmlFormatter())
            case "html-formatter":
                from .views.formatter import FormatterView
                from .formatters.html import HtmlFormatter
                tools_with_ui[tool_id]["child"] = FormatterView(HtmlFormatter())
            case "js-formatter":
                from .views.formatter import FormatterView
                from .formatters.js import JsFormatter
                tools_with_ui[tool_id]["child"] = FormatterView(JsFormatter())
            case "css-formatter":
                from .views.formatter import FormatterView
                from .formatters.css import CssFormatter
                tools_with_ui[tool_id]["child"] = FormatterView(CssFormatter())
            case "css-minifier":
                from .views.formatter import FormatterView
                from .formatters.css_minifier import CssMinifier
                tools_with_ui[tool_id]["child"] = FormatterView(CssMinifier())
            case "js-minifier":
                from .views.formatter import FormatterView
                from .formatters.js_minifier import JsMinifier
                tools_with_ui[tool_id]["child"] = FormatterView(JsMinifier())
            
            # Generators
            case "hash-generator":
                from .views.hash_generator import HashGeneratorView
                tools_with_ui[tool_id]["child"] = HashGeneratorView()
            case "lorem-generator":
                from .views.lorem_generator import LoremGeneratorView
                tools_with_ui[tool_id]["child"] = LoremGeneratorView()
            case "uuid-generator":
                from .views.uuid_generator import UuidGeneratorView
                tools_with_ui[tool_id]["child"] = UuidGeneratorView()
            case "random-generator":
                from .views.random_generator import RandomGeneratorView
                tools_with_ui[tool_id]["child"] = RandomGeneratorView()
            case "chmod":
                from .views.chmod_calculator import ChmodCalculatorView
                tools_with_ui[tool_id]["child"] = ChmodCalculatorView()
            case "qrcode":
                from .views.qrcode_generator import QRCodeGeneratorView
                tools_with_ui[tool_id]["child"] = QRCodeGeneratorView()
            
            # Text
            case "text-inspector":
                from .views.text_inspector import TextInspectorView
                tools_with_ui[tool_id]["child"] = TextInspectorView()
            case "regex-tester":
                from .views.regex_tester import RegexTesterView
                tools_with_ui[tool_id]["child"] = RegexTesterView()
            case "text-diff":
                from .views.text_diff import TextDiffView
                tools_with_ui[tool_id]["child"] = TextDiffView()
            case "xml-validator":
                from .views.xml_validator import XmlValidatorView
                tools_with_ui[tool_id]["child"] = XmlValidatorView()
            case "json-validator":
                from .views.json_validator import JsonValidatorView
                tools_with_ui[tool_id]["child"] = JsonValidatorView()
            case "markdown-preview":
                from .views.markdown_preview import MarkdownPreviewView
                tools_with_ui[tool_id]["child"] = MarkdownPreviewView()
                
            # Graphics
            case "color-converter":
                from .views.color_converter import ColorConverterView
                tools_with_ui[tool_id]["child"] = ColorConverterView()
            case "contrast-checker":
                from .views.contrast_checker import ContrastCheckerView
                tools_with_ui[tool_id]["child"] = ContrastCheckerView()
            case "colorblind-sim":
                from .views.colorblindness_simulator import ColorblindnessSimulatorView
                tools_with_ui[tool_id]["child"] = ColorblindnessSimulatorView()
            case "image-converter":
                from .views.image_converter import ImageConverterView
                tools_with_ui[tool_id]["child"] = ImageConverterView()
                
            # Certificates
            case "certificate-parser":
                from .views.certificate_parser import CertificateParserView
                tools_with_ui[tool_id]["child"] = CertificateParserView()
            case "csr-generator":
                from .views.certificate_request_generator import CertificateRequestGeneratorView
                tools_with_ui[tool_id]["child"] = CertificateRequestGeneratorView()

    return tools_with_ui

def search_tools(search_terms: List[str]) -> List[str]:
    """
    Search tools by keywords and return matching tool ids.
    """
    
    if not search_terms:
        return []
    
    search_query = " ".join(search_terms).lower()
    results = []
    
    for tool_id, tool_meta in TOOLS_METADATA.items():
        title = tool_meta["title"].lower()
        tooltip = tool_meta["tooltip"].lower()
        category = tool_meta["category"].lower()
        keywords = " ".join(tool_meta.get("keywords", [])).lower()

        if (search_query in title or
            search_query in tooltip or
            search_query in category or
            search_query in keywords):
            results.append(tool_id)
            
    return results
