# lorem_ipsum_generator.py
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

import lorem

class LoremIpsumGenerator():

    @staticmethod
    def generate_words(quantity):
        return lorem.get_word(count=quantity)

    @staticmethod
    def generate_senctences(quantity):
        return lorem.get_sentence(count=quantity)

    @staticmethod
    def generate_paragraphs(quantity):
        return lorem.get_paragraph(count=quantity)
