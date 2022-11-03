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
import io

class HashGenerator():

    @staticmethod
    def file_to_md5(file_path):
        md5 = hashlib.md5()
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                md5.update(chunk)
        return md5.hexdigest()

    @staticmethod
    def file_to_sha1(file_path):
        sha1 = hashlib.sha1()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(65536) # 64kb chunks
                if not data:
                    break
                sha1.update(data)

        return sha1.hexdigest()

    @staticmethod
    def file_to_sha256(file_path):
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(65536) # 64kb chunks
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()

    @staticmethod
    def file_to_sha512(file_path):
        sha512 = hashlib.sha512()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(65536) # 64kb chunks
                if not data:
                    break
                sha512.update(data)

        return sha512.hexdigest()


    @staticmethod
    def to_md5(input):
        return hashlib.md5(input.encode("utf-8")).hexdigest()

    @staticmethod
    def to_sha1(input):
        return hashlib.sha1(input.encode("utf-8")).hexdigest()

    @staticmethod
    def to_sha256(input):
        return hashlib.sha256(input.encode("utf-8")).hexdigest()
    
    @staticmethod
    def to_sha512(input):
        return hashlib.sha512(input.encode("utf-8")).hexdigest()

    