# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .formatter import Formatter
from gettext import gettext as _, pgettext as C_
from typing import List
import sqlparse


class SqlFormatter(Formatter):

    _title = _("SQL Formatter")
    _description = _("Format SQL documents")
    _utility_name = "sql-formatter"
    _textarea_name = _("Type SQL code here")
    _language = "sql"
    _extensions = ["sql"]
    _action_btn_name = C_("verb/action", "Format")
    _show_options = True

    def _format(self, text:str, indents:int):
        try:
            return sqlparse.format(
                text,
                indent_width=indents,
                keyword_case="upper",
                identifier_case="lower",
                reindent=True
            )
        except sqlparse.exceptions.SQLParseError:
            return ""

    def is_correct(self, text:str):
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