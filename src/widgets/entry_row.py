# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk, Gio


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/widgets/entry_row.ui")
class EntryRow(Adw.EntryRow):
    __gtype_name__ = "EntryRow"

    # Template elements
    _generate_btn = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()

    # Properties
    show_clear_btn = GObject.Property(type=bool, default=False)
    show_copy_btn = GObject.Property(type=bool, default=False)
    show_paste_btn = GObject.Property(type=bool, default=False)
    show_generate_btn = GObject.Property(type=bool, default=False)

    # Custom signals
    __gsignals__ = {
        "cleared": (GObject.SIGNAL_RUN_LAST, None, ()),
        "generate-clicked": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self):
        super().__init__()

        # Property binding
        self.bind_property("show-copy-btn", self._copy_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-paste-btn", self._paste_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-clear-btn", self._clear_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-generate-btn", self._generate_btn, "visible", GObject.BindingFlags.SYNC_CREATE)

        # Signals
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._clear_btn.connect("clicked", self._on_clear_clicked)
        self._generate_btn.connect("clicked", self._on_generate_clicked)

    def _on_copy_clicked(self, user_data:GObject.GPointer):
        text = self.get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def _on_paste_clicked(self, user_data:GObject.GPointer):
        self.clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        self.clipboard.read_text_async(None, self._on_clipboard_read_done, None)

    def _on_clipboard_read_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        string = self.clipboard.read_text_finish(result)
        self.set_text(string)

    def _on_clear_clicked(self, user_data:GObject.GPointer):
        self._clear()

    def _on_generate_clicked(self, user_data:GObject.GPointer):
        self.emit("generate-clicked")

    def _clear(self):
        self.remove_css_class("border-red")
        self.set_text("")
        self.emit("cleared")

    def clear(self):
        self._clear()
