# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from ruamel import yaml


class JSON2YAML():

    @staticmethod
    def is_text(input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    @staticmethod
    def is_json(input):
        try:
            json.loads(input)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def is_yaml(input):
        try:
            yaml.load(input, Loader=yaml.Loader)
            return True
        except yaml.YAMLError:
            return False

    @staticmethod
    def to_json(yaml_input, indents):
        return json.dumps(
            yaml.load(yaml_input, Loader=yaml.Loader),
            indent=indents,
            ensure_ascii=False
        )

    @staticmethod
    def to_yaml(input_json, indents):
        return yaml.dump(
            json.loads(input_json),
            indent=indents,
            default_flow_style=False
        )
