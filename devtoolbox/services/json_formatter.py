# json_formater.py
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