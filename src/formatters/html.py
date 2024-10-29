# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .formatter import Formatter
from gettext import gettext as _, pgettext as C_
from typing import List

from lxml import etree, html


class HtmlFormatter(Formatter):

    _title = _("HTML Formatter")
    _description = _("Format HTML documents")
    _utility_name = "html-formatter"
    _textarea_name = _("Type HTML code here")
    _language = "html"
    _extensions = ["html", "htm"]
    _action_btn_name = C_("verb/action", "Format")
    _show_options = True

    def _format(self, text:str, indents:int):
        indent_str = ""
        for _ in range(0, indents):
            indent_str += " "

        doc_root = html.fromstring(text)
        etree.indent(doc_root, space=indent_str)
        return etree.tostring(doc_root, encoding='unicode', pretty_print=True)

    def is_correct(self, text:str) -> bool:
        if isinstance(text, str):
            return True
        else:
            try:
                text.decode("utf-8")
                return True
            except UnicodeError:
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

    def get_action_button_name(self) -> str:
        return self._action_btn_name
    
    def get_show_options(self) -> bool:
        return self._show_options