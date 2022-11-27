# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json


class JsonFormatter():

    def get_name(self):
        return "JSON"
    
    def get_utility_name(self):
        return "jsonformatter"

    def get_file_extensions(self):
        return ["json"]

    def is_text(self, input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    def indent(self, input, indents):
        try:
            return True, json.dumps(json.loads(input), indent=indents)
        except json.JSONDecodeError:
            return False, ""