# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .formatter import Formatter
from gettext import gettext as _
from typing import List
import cssbeautifier


class CssFormatter(Formatter):

    _title = _("CSS Formatter")
    _description = _("Format CSS documents")
    _utility_name = "css-formatter"
    _textarea_name = _("Type CSS here")
    _language = "css"
    _extensions = ["css", "scss", "sass"]

    def _format(self, text:str, indents:int):
        opts = cssbeautifier.default_options()
        opts.indent_size = indents
        return cssbeautifier.beautify(text, opts)

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
