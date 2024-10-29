
# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .formatter import Formatter
from gettext import gettext as _, pgettext as C_
from typing import List
import rjsmin


class JsMinifier(Formatter):

    _title = _("JavaScript Minifier")
    _description = _("Minify JS code")
    _utility_name = "js-minifier"
    _textarea_name = _("Type JS code here")
    _language = "js"
    _extensions = ["js", "mjs", "ts", "tsx"]
    _action_btn_name = C_("verb/action", "Minify")
    _show_options = False

    def _format(self, text:str, indents:int):
        return rjsmin.jsmin(text)

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