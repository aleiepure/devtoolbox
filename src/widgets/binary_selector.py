# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/binary_selector.ui')
class BinarySelector(Adw.Bin):
    __gtype_name__ = "BinarySelector"

    # Template Elements
    _left_btn = Gtk.Template.Child()
    _right_btn = Gtk.Template.Child()

    # Properties
    left_lbl = GObject.Property(type=str, default="")
    right_lbl = GObject.Property(type=str, default="")
    left_btn_active = GObject.Property(type=bool, default=True)
    right_btn_active = GObject.Property(type=bool, default=False)

    # Custom signals
    __gsignals__ = {
        "toggled": (GObject.SIGNAL_RUN_LAST, None, ())
    }

    def __init__(self):
        super().__init__()

        # Property binding
        self.bind_property("left-lbl",   self._left_btn,  "label",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("right-lbl",  self._right_btn, "label",  GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("left-btn-active",  self._left_btn,  "active", GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property("right-btn-active", self._right_btn, "active", GObject.BindingFlags.BIDIRECTIONAL)
        self._left_btn.bind_property("active", self._right_btn, "active", GObject.BindingFlags.INVERT_BOOLEAN)
        self._right_btn.bind_property("active", self._left_btn, "active", GObject.BindingFlags.INVERT_BOOLEAN)

        # Signals
        self._left_btn.connect("toggled", self._on_toggled)

    def _on_toggled(self, user_data):
        self.emit("toggled")

    def get_left_btn_active(self) -> bool:
        return self.left_btn_active

    def get_right_btn_active(self) -> bool:
        return self.right_btn_active

    def get_left_btn(self) -> Gtk.Button:
        return self._left_btn

    def get_right_btn(self) -> Gtk.Button:
        return self._right_btn
