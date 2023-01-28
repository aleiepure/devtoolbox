# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/binary_selector.ui')
class BinarySelector(Adw.Bin):
    __gtype_name__ = "BinarySelector"

    # Template Elements
    _left_btn  = Gtk.Template.Child()
    _right_btn = Gtk.Template.Child()

    # Properties
    left_label   = GObject.Property(type=str, default="")
    right_label  = GObject.Property(type=str, default="")
    left_active  = GObject.Property(type=bool, default=True)
    right_active = GObject.Property(type=bool, default=False)

    # Custom signals
    __gsignals__ = {
        "toggled": (GObject.SIGNAL_RUN_LAST, None, ())
    }

    def __init__(self):
        super().__init__()

        # Property binding
        self.bind_property("left-label",   self._left_btn,  "label",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("right-label",  self._right_btn, "label",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("left-active",  self._left_btn,  "active", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("right-active", self._right_btn, "active", GObject.BindingFlags.SYNC_CREATE)
        self._left_btn.bind_property("active", self._right_btn, "active", GObject.BindingFlags.INVERT_BOOLEAN)
        self._right_btn.bind_property("active", self._left_btn, "active", GObject.BindingFlags.INVERT_BOOLEAN)

        # Signals
        self._left_btn.connect("toggled", self._on_toggled)

    def _on_toggled(self, data):
        self.emit("toggled")

    def get_left_active(self) -> bool:
        return self._left_btn.get_active()

    def get_right_active(self) -> bool:
        return self._right_btn.get_active()

    def get_left_button(self) -> Gtk.Button:
        return self._left_btn

    def get_right_button(self) -> Gtk.Button:
        return self._right_btn
