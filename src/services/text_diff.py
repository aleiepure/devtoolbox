# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject, Gtk, GLib
import difflib
from typing import List, Dict


class TextDiffService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_text1(self, text1:str):
        self._text1 = text1

    def set_text2(self, text2:str):
        self._text2 = text2

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._buffer = None
        self._text1 = None
        self._text2 = None
        return result.propagate_value().value

    def find_diff_and_tag_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._find_diff_and_tag_thread)

    def _find_diff_and_tag_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._find_diff_and_tag(self._text1, self._text2)
        task.return_value(outcome)

    def _find_diff_and_tag(self, text1:str, text2:str):
        diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
        return self._get_output(diff)

    def _get_output(self, diff):
        output = ""
        items_to_tag = []
        items_to_tag_dict = {} # {line: xx, tag: +/-, length: xx, chars_to_tag: []}
        line_nr = 0
        current_tag_type = ""

        for line in diff:
            if line:
                match line[0]: # Check first character
                    case "-":
                        items_to_tag = self._append_to_dict_list(items_to_tag, line_nr, '-', len(line[2:]), [])
                        current_tag_type = "-"
                        output += line[2:] + "\n"
                        line_nr += 1
                    case "+":
                        items_to_tag = self._append_to_dict_list(items_to_tag, line_nr, '+', len(line[2:]), [])
                        current_tag_type = "+"
                        output += line[2:] + "\n"
                        line_nr += 1
                    case "?":
                        chars_to_tag = [i-2 for i, x in enumerate(line) if current_tag_type == x]
                        items_to_tag = self._append_to_dict_list(items_to_tag, line_nr-1, current_tag_type, -1, chars_to_tag)
                    case other:
                        output += line[2:] + "\n"
                        line_nr += 1

        return output, items_to_tag

    def _append_to_dict_list(self, list_of_dict:List[Dict], line_nr:int, tag_type:str, length:int, chars_to_tag:List[int]) -> List[Dict]:
        tmp_dict = {
            "line": line_nr,
            "tag": tag_type,
            "length": length,
            "chars_to_tag": chars_to_tag
        }
        list_of_dict.append(tmp_dict)
        return list_of_dict
