# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gdk, GObject, Gio, GLib
import textstat

from ..services.text_inspector import TextInspectorService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/text_inspector.ui")
class TextInspectorView(Adw.Bin):
    __gtype_name__ = "TextInspectorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _original_case_btn = Gtk.Template.Child()
    _sentence_case_btn = Gtk.Template.Child()
    _lower_case_btn = Gtk.Template.Child()
    _upper_case_btn = Gtk.Template.Child()
    _title_case_btn = Gtk.Template.Child()
    _camel_case_btn = Gtk.Template.Child()
    _pascal_case_btn = Gtk.Template.Child()
    _snake_case_btn = Gtk.Template.Child()
    _constant_case_btn = Gtk.Template.Child()
    _kebab_case_btn = Gtk.Template.Child()
    _cobol_case_btn = Gtk.Template.Child()
    _train_case_btn = Gtk.Template.Child()
    _alternating_case_btn = Gtk.Template.Child()
    _reverse_alternating_case_btn = Gtk.Template.Child()
    _line_lbl = Gtk.Template.Child()
    _column_lbl = Gtk.Template.Child()
    _chars_lbl = Gtk.Template.Child()
    _words_lbl = Gtk.Template.Child()
    _lines_lbl = Gtk.Template.Child()
    _textarea = Gtk.Template.Child()

    _service = TextInspectorService()

    def __init__(self):
        super().__init__()

        # Signals
        self._original_case_btn.connect("clicked", self._on_original_case_btn_clicked)
        self._sentence_case_btn.connect("clicked", self._on_sentence_case_btn_clicked)
        self._lower_case_btn.connect("clicked", self._on_lower_case_btn_clicked)
        self._upper_case_btn.connect("clicked", self._on_upper_case_btn_clicked)
        self._title_case_btn.connect("clicked", self._on_title_case_btn_clicked)
        self._camel_case_btn.connect("clicked", self._on_camel_case_btn_clicked)
        self._pascal_case_btn.connect("clicked", self._on_pascal_case_btn_clicked)
        self._snake_case_btn.connect("clicked", self._on_snake_case_btn_clicked)
        self._constant_case_btn.connect("clicked", self._on_constant_case_btn_clicked)
        self._kebab_case_btn.connect("clicked", self._on_kebab_case_btn_clicked)
        self._cobol_case_btn.connect("clicked", self._on_cobol_case_btn_clicked)
        self._train_case_btn.connect("clicked", self._on_train_case_btn_clicked)
        self._alternating_case_btn.connect("clicked", self._on_alternating_case_btn_clicked)
        self._reverse_alternating_case_btn.connect("clicked", self._on_reverse_alternating_case_btn_clicked)
        self._textarea.connect("cursor-moved", self._on_text_cursor_moved)
        self._textarea.connect("view-cleared", self._on_view_cleared)
        self._text_changed_handler = self._textarea.connect("text-changed", self._on_text_changed)

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._textarea.set_spinner_spin(False)
        self._service.get_cancellable().cancel()

    def _on_original_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_text(self._original_text)

    def _on_sentence_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_sentence_case_async(self, self._on_async_done)

    def _on_lower_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_lower_case_async(self, self._on_async_done)

    def _on_upper_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_upper_case_async(self, self._on_async_done)

    def _on_title_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_title_case_async(self, self._on_async_done)

    def _on_camel_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_camel_case_async(self, self._on_async_done)

    def _on_pascal_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_pascal_case_async(self, self._on_async_done)

    def _on_snake_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_snake_case_async(self, self._on_async_done)

    def _on_constant_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_constant_case_async(self, self._on_async_done)

    def _on_kebab_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_kebab_case_async(self, self._on_async_done)

    def _on_cobol_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_cobol_case_async(self, self._on_async_done)

    def _on_train_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_train_case_async(self, self._on_async_done)

    def _on_alternating_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_alternating_case_async(self, self._on_async_done)

    def _on_reverse_alternating_case_btn_clicked(self, user_data:GObject.GPointer):
        self._textarea.set_spinner_spin(True)
        self._service.set_text(self._original_text)
        self._service.to_reverse_alternating_case_async(self, self._on_async_done)

    def _on_text_cursor_moved(self, source_widget:GObject.Object):
        insert_mark = self._textarea.get_buffer().get_insert()
        iter_at_insert = self._textarea.get_buffer().get_iter_at_mark(insert_mark)
        self._line_lbl.set_label(str(iter_at_insert.get_line()+1))
        self._column_lbl.set_label(str(iter_at_insert.get_line_offset()+1))

    def _on_async_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        outcome = self._service.async_finish(result, self)
        self._textarea.handler_block(self._text_changed_handler)
        self._textarea.set_text(outcome)
        self._textarea.handler_unblock(self._text_changed_handler)
        self._calculate_stats()
        self._textarea.set_spinner_spin(False)

    def _on_text_changed(self, source_widget:GObject.Object):
        self._original_case_btn.set_active(True)
        text = self._textarea.get_text()
        self._original_text = text
        self._calculate_stats()

    def _calculate_stats(self):
        self._chars_lbl.set_label(str(self._textarea.get_buffer().get_char_count()))
        self._lines_lbl.set_label(str(self._textarea.get_buffer().get_line_count()))
        self._words_lbl.set_label(str(len(self._textarea.get_text().split())))
