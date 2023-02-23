# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio
from typing import List, Dict

from ..services.text_diff import TextDiffService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/text_diff.ui")
class TextDiffView(Adw.Bin):
    __gtype_name__ = "TextDiffView"

    _new_textarea = Gtk.Template.Child()
    _old_textarea = Gtk.Template.Child()
    _diff_textarea = Gtk.Template.Child()

    _service = TextDiffService()

    def __init__(self):
        super().__init__()

        self._tag_line_removed = self._diff_textarea.get_buffer().create_tag("line-removed", background="#5d2a2a")
        self._tag_line_added = self._diff_textarea.get_buffer().create_tag("line-added", background="#494f3b")
        self._tag_removed = self._diff_textarea.get_buffer().create_tag("removed", background="#7d2121")
        self._tag_added = self._diff_textarea.get_buffer().create_tag("added", background="#5b7822")

        self._diff()

        # Signals
        self._new_textarea.connect("text-changed", self._on_new_text_changed)
        self._old_textarea.connect("text-changed", self._on_old_text_changed)

    def _on_new_text_changed(self, source_widget:GObject.Object):
        self._service.get_cancellable().cancel()
        self._diff()

    def _on_old_text_changed(self, source_widget:GObject.Object):
        self._service.get_cancellable().cancel()
        self._diff()

    def _diff(self):

        # Stop previous tasks
        buffer = self._diff_textarea.get_buffer()
        self._diff_textarea.set_spinner_spin(False)
        buffer.remove_all_tags(buffer.get_start_iter(), buffer.get_end_iter())
        self._service.get_cancellable().cancel()

        # Setup task
        self._diff_textarea.set_spinner_spin(True)
        self._service.set_text1(self._old_textarea.get_text())
        self._service.set_text2(self._new_textarea.get_text())

        # Call task
        self._service.find_diff_and_tag_async(self, self._on_diff_done)

    def _on_diff_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome, items_to_tag = self._service.async_finish(result, self)
        self._diff_textarea.set_text(outcome)
        self._tag_text(items_to_tag)
        self._diff_textarea.set_spinner_spin(False)

    def _tag_text(self, items_to_tag:List[Dict]):
        for item in items_to_tag:
            if item["length"] != -1: # line
                start_gtext_iter = self._diff_textarea.get_buffer().get_iter_at_line(item["line"])[1]
                end_gtext_iter = self._diff_textarea.get_buffer().get_iter_at_line_offset(item["line"], item["length"]+1)[1]
                if item["tag"] == "+":
                    self._diff_textarea.get_buffer().apply_tag(self._tag_line_added, start_gtext_iter, end_gtext_iter)
                else:
                    self._diff_textarea.get_buffer().apply_tag(self._tag_line_removed, start_gtext_iter, end_gtext_iter)
            else: # chars
                for char in item["chars_to_tag"]:
                    start_gtext_iter = self._diff_textarea.get_buffer().get_iter_at_line_offset(item["line"], char)[1]
                    end_gtext_iter = self._diff_textarea.get_buffer().get_iter_at_line_offset(item["line"], char+1)[1]
                    if item["tag"] == "+":
                        self._diff_textarea.get_buffer().apply_tag(self._tag_added, start_gtext_iter, end_gtext_iter)
                    else:
                        self._diff_textarea.get_buffer().apply_tag(self._tag_removed, start_gtext_iter, end_gtext_iter)
