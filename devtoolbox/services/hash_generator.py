# hash_generator.py
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

import hashlib

class HashGenerator():

    @staticmethod
    def to_md5(input):
        return hashlib.md5(input).hexdigest()

    @staticmethod
    def to_sha1(input):
        return hashlib.sha1(input).hexdigest()

    @staticmethod
    def to_sha256(input):
        return hashlib.sha256(input).hexdigest()
    
    @staticmethod
    def to_sha512(input):
        return hashlib.sha512(input).hexdigest()

    