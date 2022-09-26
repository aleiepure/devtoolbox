# json2yaml.py
#
# Copyright 2022 Alessandro Iepure
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
