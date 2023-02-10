# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/widgets/entry_row.ui")
class EntryRow(Adw.EntryRow):
    __gtype_name__ = "EntryRow"

    # Template elements
    _copy_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()

    # Properties
    show_clear_btn = GObject.Property(type=bool, default=False)
    show_copy_btn = GObject.Property(type=bool, default=False)
    show_paste_btn = GObject.Property(type=bool, default=False)

    # Custom signals
    __gsignals__ = {
        "cleared": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self):
        super().__init__()

        # Property binding
        self.bind_property("show-copy-btn", self._copy_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-paste-btn", self._paste_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-clear-btn", self._clear_btn, "visible", GObject.BindingFlags.SYNC_CREATE)

        # Signals
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._clear_btn.connect("clicked", self._on_clear_clicked)

    def _on_copy_clicked(self, user_data):
        text = self.get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def _on_paste_clicked(self, user_data):
        pass # pasting via the provided button doesn't work. See known issues.

    def _on_clear_clicked(self, user_data):
        self._clear()

    def _clear(self):
        self.remove_css_class("border-red")
        self.set_text("")
        self.emit("cleared")

    def clear(self):
        self._clear()
