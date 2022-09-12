# utils.py
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

from gi.repository import Gdk, GLib


class Utils():

    @staticmethod
    def is_text(input):
        try:
            input.decode("utf-8")
            return True
        except UnicodeError:
            return False

    @staticmethod
    def is_image(input):
        try:
            Gdk.Texture.new_from_bytes(GLib.Bytes(input))
            return True
        except GLib.GError:
            return False
