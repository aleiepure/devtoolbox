# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import html


class HTMLEncoder():

    @staticmethod
    def is_text(input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    @staticmethod
    def escape(input):
        return html.escape(input)

    @staticmethod
    def unescape(input):
        return html.unescape(input)
