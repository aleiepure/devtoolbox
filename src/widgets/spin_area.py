# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/spin_area.ui')
class SpinArea(Adw.Bin):
    __gtype_name__ = 'SpinArea'

    # Template elements
    _name_lbl = Gtk.Template.Child()
    _spinner = Gtk.Template.Child()
    _spinner_separator = Gtk.Template.Child()
    _action_btn = Gtk.Template.Child()
    _action_btn_separator = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _spin_btn = Gtk.Template.Child()

    # Properties
    name = GObject.Property(type=str, default="")
    show_spinner = GObject.Property(type=bool, default=False)
    show_copy_btn = GObject.Property(type=bool, default=False)
    show_paste_btn = GObject.Property(type=bool, default=False)
    show_action_btn = GObject.Property(type=bool, default=False)
    action_btn_name = GObject.Property(type=str, default="")
    action_btn_tooltip = GObject.Property(type=str, default="")

    # Custom signals
    __gsignals__ = {
        "action-clicked": (GObject.SIGNAL_RUN_LAST, None, ()),
        "value-changed": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "spinarea")

        # Property binding
        self.bind_property("name", self._name_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner_separator, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-copy-btn", self._copy_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-paste-btn", self._paste_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-action-btn", self._action_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-action-btn", self._action_btn_separator, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("action-btn-name", self._action_btn, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("action-btn-tooltip", self._action_btn, "tooltip-text", GObject.BindingFlags.SYNC_CREATE)
        self._spinner.bind_property("visible", self._spinner_separator, "visible", GObject.BindingFlags.BIDIRECTIONAL)
        self._action_btn.bind_property("visible", self._action_btn_separator, "visible", GObject.BindingFlags.BIDIRECTIONAL)

        # Signal connection
        self._action_btn.connect("clicked", self._on_action_clicked)
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._spin_btn.connect("value-changed", self._on_value_changed)

    def _on_action_clicked(self, user_data:GObject.GPointer):
        self.emit("action-clicked")

    def _on_copy_clicked(self, user_data:GObject.GPointer):
        text      = str(self._spin_btn.get_value_as_int())
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def _on_paste_clicked(self, user_data:GObject.GPointer):
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.read_text_async(
            None,
            self._on_paste_done,
            None
        )

    def _on_paste_done(self, clipboard:Gdk.Clipboard, res, data:GObject.GPointer):
        text = clipboard.read_text_finish(res)
        if text:
            try:
                value = int(text)
                self._spin_btn.set_value(value)
            except ValueError:
                pass

    def _on_value_changed(self, user_data:GObject.GPointer):
        self.emit("value-changed")

    def get_value(self) -> int:
        return self._spin_btn.get_value_as_int()

    def set_value(self, value:int):
        self._spin_btn.set_value(value)
