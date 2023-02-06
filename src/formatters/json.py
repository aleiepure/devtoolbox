# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .formatter import Formatter
from gettext import gettext as _
import json
from typing import List


class JsonFormatter(Formatter):

    _title = _("JSON Formatter")
    _description = _("Format JSON documents")
    _utility_name = "json-formatter"
    _textarea_name = _("Type JSON code here")
    _language = "json"
    _extensions = ["json"]

    def _format(self, text:str, indents:int):
        try:
            return json.dumps(json.loads(text), indent=indents)
        except json.JSONDecodeError:
            return ""

    def is_correct(self, text:str):
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
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
