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
        ],
        "widget_class": "devtoolbox.views.json_yaml_toml.JsonYamlTomlView"
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
        ],
        "widget_class": "devtoolbox.views.timestamp.TimestampView"
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
        ],
        "widget_class": "devtoolbox.views.base_converter.BaseConverterView"
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
        ],
        "widget_class": "devtoolbox.views.cron_converter.CronConverterView"
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
        ],
        "widget_class": "devtoolbox.views.reverse_cron.ReverseCronView"
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
        ],
        "widget_class": "devtoolbox.views.html_encoder.HtmlEncoderView"
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
        ],
        "widget_class": "devtoolbox.views.base64_encoder.Base64EncoderView"
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
        ],
        "widget_class": "devtoolbox.views.url_encoder.UrlEncoderView"
    },
    "gzip-compressor": {
        "title": "GZip",
        "category": _("Encoders & Decoders"),
        "icon-name": "shoe-box-symbolic",
        "tooltip": _("Compress and decompress files and texts using GZip"),
        "keywords": [
            C_("search keyword", "gzip"),
            C_("search keyword", "compression"),
            C_("search keyword", "archive"),
            C_("search keyword", "file"),
            C_("search keyword", "text"),
        ],
        "compressor_class": "devtoolbox.compressors.gzip_compressor.GzipCompressor"
    },
    "lzma-compressor": {
        "title": "LZMA",
        "category": _("Encoders & Decoders"),
        "icon-name": "shoe-box-symbolic",
        "tooltip": _("Compress and decompress files and texts using LZMA"),
        "keywords": [
            C_("search keyword", "lzma"),
            C_("search keyword", "xz"),
            C_("search keyword", "compression"),
            C_("search keyword", "archive"),
            C_("search keyword", "file"),
            C_("search keyword", "text"),
        ],
        "compressor_class": "devtoolbox.compressors.lzma_compressor.LzmaCompressor"
    },
    "bz2-compressor": {
        "title": "Bzip2",
        "category": _("Encoders & Decoders"),
        "icon-name": "shoe-box-symbolic",
        "tooltip": _("Compress and decompress files and texts using Bzip2"),
        "keywords": [
            C_("search keyword", "bzip2"),
            C_("search keyword", "bz2"),
            C_("search keyword", "compression"),
            C_("search keyword", "archive"),
            C_("search keyword", "file"),
            C_("search keyword", "text"),
        ],
        "compressor_class": "devtoolbox.compressors.bz2_compressor.Bz2Compressor"
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
        ],
        "widget_class": "devtoolbox.views.jwt_decoder.JwtDecoderView"
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
        ],
        "formatter_class": "devtoolbox.formatters.json.JsonFormatter"
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
        ],
        "formatter_class": "devtoolbox.formatters.sql.SqlFormatter"
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
        ],
        "formatter_class": "devtoolbox.formatters.xml.XmlFormatter"
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
        ],
        "formatter_class": "devtoolbox.formatters.html.HtmlFormatter"
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
        ],
        "formatter_class": "devtoolbox.formatters.js.JsFormatter"
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
        ],
        "formatter_class": "devtoolbox.formatters.css.CssFormatter"
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
        ],
        "formatter_class": "devtoolbox.formatters.css_minifier.CssMinifier"
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
        ],
        "formatter_class": "devtoolbox.formatters.js_minifier.JsMinifier"
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
        ],
        "widget_class": "devtoolbox.views.hash_generator.HashGeneratorView"
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
        ],
        "widget_class": "devtoolbox.views.lorem_generator.LoremGeneratorView"
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
        ],
        "widget_class": "devtoolbox.views.uuid_generator.UuidGeneratorView"
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
        ],
        "widget_class": "devtoolbox.views.random_generator.RandomGeneratorView"
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
        ],
        "widget_class": "devtoolbox.views.chmod_calculator.ChmodCalculatorView"
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
        ],
        "widget_class": "devtoolbox.views.qrcode_generator.QRCodeGeneratorView"
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
        ],
        "widget_class": "devtoolbox.views.text_inspector.TextInspectorView"
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
        ],
        "widget_class": "devtoolbox.views.regex_tester.RegexTesterView"
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
        ],
        "widget_class": "devtoolbox.views.text_diff.TextDiffView"
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
        ],
        "widget_class": "devtoolbox.views.xml_validator.XmlValidator"
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
        ],
        "widget_class": "devtoolbox.views.json_validator.JsonValidatorView"
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
        ],
        "widget_class": "devtoolbox.views.markdown_preview.MarkdownPreviewView"
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
        ],
        "widget_class": "devtoolbox.views.color_converter.ColorConverterView"
    },
    "contrast-checker": {
        "title": _("Contrast Checker"),
        "category": _("Graphics"),
        "icon-name": "image-adjust-contrast-symbolic",
        "tooltip": _("Check a color combination for WCAG compliance"),
        "keywords": [
            C_("search keyword", "accessibility"),
            C_("search keyword", "ratio"),
        ],
        "widget_class": "devtoolbox.views.contrast_checker.ContrastCheckerView"
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
        ],
        "widget_class": "devtoolbox.views.colorblindness_simulator.ColorblindnessSimulatorView"
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
        ],
        "widget_class": "devtoolbox.views.image_converter.ImageConverterView"
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
        ],
        "widget_class": "devtoolbox.views.certificate_parser.CertificateParserView"
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
        ],
        "widget_class": "devtoolbox.views.certificate_request_generator.CertificateRequestGeneratorView"
    },
}


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
