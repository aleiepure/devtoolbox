# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import jwt


class JwtDecoder():

    @staticmethod
    def is_text(input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    @staticmethod
    def convert(token):
        try:
            header = json.dumps(jwt.get_unverified_header(token), indent=4)
            payload = json.dumps(jwt.decode(
                token, options={"verify_signature": False}), indent=4)
            return True, header, payload
        except jwt.exceptions.DecodeError:
            return False, "", ""
