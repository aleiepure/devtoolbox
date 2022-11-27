# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
