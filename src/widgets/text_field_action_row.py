# Copyright (C) 2022-2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk
from gettext import gettext as _


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/text_field_action_row.ui')
class TextFieldActionRow(Adw.ActionRow):
    __gtype_name__ = "TextFieldActionRow"

    # Template elements
    _stack       = Gtk.Template.Child()
    _loadind_lbl = Gtk.Template.Child()
    _textfield   = Gtk.Template.Child()
    _separator   = Gtk.Template.Child()
    _copy_btn    = Gtk.Template.Child()
    _paste_btn   = Gtk.Template.Child()
    _clear_btn   = Gtk.Template.Child()

    # Custom properties
    text_editable = GObject.Property(type=bool, default=True)
    show_copy_btn = GObject.Property(type=bool, default=False)
    show_paste_btn = GObject.Property(type=bool, default=False)
    show_clear_btn = GObject.Property(type=bool, default=False)

    # Custom signals
    __gsignals__ = {
        "text-changed": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self):
        super().__init__()

        # Separator visibility
        if self.show_copy_btn or self.show_paste_btn or self.show_clear_btn:
            self._separator.set_visible(True)
        else:
            self._separator.set_visible(False)

        # Property binding
        self.bind_property("text_editable",  self._textfield, "editable", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show_copy_btn",  self._copy_btn,  "visible",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show_copy_btn",  self._separator, "visible",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show_paste_btn", self._paste_btn, "visible",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show_paste_btn", self._separator, "visible",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show_clear_btn", self._clear_btn, "visible",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show_clear_btn", self._separator, "visible",  GObject.BindingFlags.SYNC_CREATE)

        # Signals
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._clear_btn.connect("clicked", self._on_clear_clicked)
        self._textfield.connect("notify::text", self._on_text_changed)

    def _on_copy_clicked(self, data):
        text      = self._text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def _on_paste_clicked(self, data):
        self._textfield.emit("paste-clipboard")

    def _on_clear_clicked(self, data):
        self._text.set_text("")

    def _on_text_changed(self, widget, data):
        self.emit("text-changed")

    def set_text(self, text):
        self._text.get_buffer().set_text(text, -1)

    def get_text(self) -> str:
        return self._text.get_buffer().get_text()

    def set_loading_visible(self, enabled:bool, label:str):
        if enabled:
            self.loading_lbl = label
            self._stack.set_visible_child_name("loading")
        else:
            self._stack.set_visible_child_name("text-area")
