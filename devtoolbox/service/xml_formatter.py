# xml_formater.py
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

import lxml.etree
import xml.etree.ElementTree as etree


class XmlFormatter():

    def get_name(self):
        return "XML"

    def get_settings_name(self):
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
