# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import lxml.etree
import xml.etree.ElementTree as etree


class XmlFormatter():

    def get_name(self):
        return "XML"

    def get_utility_name(self):
        return "xmlformatter"

    def get_file_extensions(self):
        return ["xml"]

    def is_text(self, input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    def indent(self, input, indents):
        indent_str = ""
        for _ in range(0, indents):
            indent_str += " "

        try:
            xml = etree.XML(input)
            etree.indent(xml, space=indent_str)
            #return True, lxml.etree.tostring(lxml.etree.fromstring(input.encode("utf-8")), pretty_print=True, encoding="utf-8", xml_declaration="True").decode("utf-8")
            return True, etree.tostring(xml, encoding="utf-8", xml_declaration=True).decode("utf-8")
        except lxml.etree.XMLSyntaxError:
            return False, ""
