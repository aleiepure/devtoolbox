# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from urllib import parse


class URLEncoder():

    @staticmethod
    def is_text(input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    @staticmethod
    def encode(input, space_as_plus):
        if space_as_plus:
            return parse.quote_plus(input)

        return parse.quote(input)

    @staticmethod
    def decode(input):
        return parse.unquote_plus(input)