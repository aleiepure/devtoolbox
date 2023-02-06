# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .formatter import Formatter
from gettext import gettext as _
from typing import List

import lxml.etree
import xml.etree.ElementTree as etree


class XmlFormatter(Formatter):

    _title = _("XML Formatter")
    _description = _("Format XML documents")
    _utility_name = "xml-formatter"
    _textarea_name = _("Type XML code here")
    _language = "xml"
    _extensions = ["xml", "html", "htm", "svg"]

    def _format(self, text:str, indents:int):
        indent_str = ""
        for _ in range(0, indents):
            indent_str += " "

        try:
            xml = etree.XML(text)
            etree.indent(xml, space=indent_str)
            return etree.tostring(xml, encoding="utf-8", xml_declaration=True).decode("utf-8")
        except lxml.etree.XMLSyntaxError:
            return ""

    def is_correct(self, text:str) -> bool:
        try:
            etree.XML(text)
            return True
        except etree.ParseError:
            return False

    def get_title(self) -> str:
        return self._title

    def get_description(self) -> str:
        return self._description

    def get_utility_name(self) -> str:
        return self._utility_name

    def get_textarea_name(self) -> str:
        return self._textarea_name

    def get_language(self) -> str:
        return self._language

    def get_file_extensions(self) -> List[str]:
        return self._extensions
