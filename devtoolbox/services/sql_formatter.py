# Copyright (C) 2022 Alessandro Iepure
# 
# SPDX-License-Identifier: GPL-3.0-or-later

import sqlparse


class SqlFormatter():

    def get_name(self):
        return "SQL"

    def get_utility_name(self):
        return "sqlformatter"

    def get_file_extensions(self):
        return ["sql"]

    def is_text(self, input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    def indent(self, input, indents):
        try:
            return True, sqlparse.format(
                input,
                indent_width=indents,
                keyword_case="upper",
                identifier_case="lower",
                reindent=True
            )
        except sqlparse.exceptions.SQLParseError:
            return False, ""
