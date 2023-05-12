# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject

from ..utils import Utils



@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/chmod_calculator.ui")
class ChmodCalculatorView(Adw.Bin):
    __gtype_name__ = "ChmodCalculatorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _owner_read_btn = Gtk.Template.Child()
    _owner_write_btn = Gtk.Template.Child()
    _owner_execute_btn = Gtk.Template.Child()
    _group_read_btn = Gtk.Template.Child()
    _group_write_btn = Gtk.Template.Child()
    _group_execute_btn = Gtk.Template.Child()
    _others_read_btn = Gtk.Template.Child()
    _others_write_btn = Gtk.Template.Child()
    _others_execute_btn = Gtk.Template.Child()
    _numeric_row = Gtk.Template.Child()
    _symbolic_row = Gtk.Template.Child()

    _invalid_toast = Adw.Toast(title=_("Invalid value. Please check again"))


    def __init__(self):
        super().__init__()

        # Signals
        self._owner_read_handler = self._owner_read_btn.connect("toggled", self._on_button_toggled)
        self._owner_write_handler = self._owner_write_btn.connect("toggled", self._on_button_toggled)
        self._owner_execute_handler = self._owner_execute_btn.connect("toggled", self._on_button_toggled)
        self._group_read_handler = self._group_read_btn.connect("toggled", self._on_button_toggled)
        self._group_write_handler = self._group_write_btn.connect("toggled", self._on_button_toggled)
        self._group_execute_handler = self._group_execute_btn.connect("toggled", self._on_button_toggled)
        self._others_read_handler = self._others_read_btn.connect("toggled", self._on_button_toggled)
        self._others_write_handler = self._others_write_btn.connect("toggled", self._on_button_toggled)
        self._others_execute_handler = self._others_execute_btn.connect("toggled", self._on_button_toggled)
        self._numeric_handler = self._numeric_row.connect("changed", self._on_numeric_entry_changed)
        self._symbolic_handler = self._symbolic_row.connect("changed", self._on_symbolic_entry_changed)

    def _on_button_toggled(self, user_date: GObject.GPointer):
        value = 0
        symbolic = list("---------")
        if self._owner_read_btn.get_active():
            value += 400
            symbolic[0] = "r"
        if self._owner_write_btn.get_active():
            value += 200
            symbolic[1] = "w"
        if self._owner_execute_btn.get_active():
            value += 100
            symbolic[2] = "x"
        if self._group_read_btn.get_active():
            value += 40
            symbolic[3] = "r"
        if self._group_write_btn.get_active():
            value += 20
            symbolic[4] = "w"
        if self._group_execute_btn.get_active():
            value += 10
            symbolic[5] = "x"
        if self._others_read_btn.get_active():
            value += 4
            symbolic[6] = "r"
        if self._others_write_btn.get_active():
            value += 2
            symbolic[7] = "w"
        if self._others_execute_btn.get_active():
            value += 1
            symbolic[8] = "x"

        self._block_all_handlers()

        self._numeric_row.set_text(str(f"{value:03d}"))
        self._symbolic_row.set_text("".join(symbolic))

        self._unblock_all_handlers()

    def _uncheck_btns(self):
        self._owner_read_btn.set_active(False)
        self._owner_write_btn.set_active(False)
        self._owner_execute_btn.set_active(False)
        self._group_read_btn.set_active(False)
        self._group_write_btn.set_active(False)
        self._group_execute_btn.set_active(False)
        self._others_read_btn.set_active(False)
        self._others_write_btn.set_active(False)
        self._others_execute_btn.set_active(False)

    def _on_numeric_entry_changed(self, user_date: GObject.GPointer):
        self._numeric_row.remove_css_class("border-red")

        self._block_all_handlers()
        self._uncheck_btns()
        self._unblock_all_handlers()

        if len(self._numeric_row.get_text()) == 3:
            if not Utils.is_numeric_chmod(int(self._numeric_row.get_text())):
                self._numeric_row.add_css_class("border-red")
                self._block_all_handlers()
                self._symbolic_row.set_text("")
                self._unblock_all_handlers()
                self._toast.add_toast(self._invalid_toast)
                return
            else:
                l = list(self._numeric_row.get_text())
                owner = int(l[0])
                group = int(l[1])
                others = int(l[2])

                # Owner
                if owner - 4 >= 0:
                    owner -= 4
                    self._block_all_handlers()
                    self._owner_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if owner - 2 >= 0:
                    owner -= 2
                    self._block_all_handlers()
                    self._owner_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if owner - 1 >= 0:
                    owner -= 1
                    self._block_all_handlers()
                    self._owner_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Group
                if group - 4 >= 0:
                    group -= 4
                    self._block_all_handlers()
                    self._group_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if group - 2 >= 0:
                    group -= 2
                    self._block_all_handlers()
                    self._group_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if group - 1 >= 0:
                    group -= 1
                    self._block_all_handlers()
                    self._group_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Others
                if others - 4 >= 0:
                    others -= 4
                    self._block_all_handlers()
                    self._others_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if others - 2 >= 0:
                    others -= 2
                    self._block_all_handlers()
                    self._others_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if others - 1 >= 0:
                    others -= 1
                    self._block_all_handlers()
                    self._others_execute_btn.set_active(True)
                    self._unblock_all_handlers()
        else:
            self._numeric_row.add_css_class("border-red")

    def _block_all_handlers(self):
        self._owner_write_btn.handler_block(self._owner_write_handler)
        self._owner_read_btn.handler_block(self._owner_read_handler)
        self._owner_execute_btn.handler_block(self._owner_execute_handler)
        self._group_write_btn.handler_block(self._group_write_handler)
        self._group_read_btn.handler_block(self._group_read_handler)
        self._group_execute_btn.handler_block(self._group_execute_handler)
        self._others_write_btn.handler_block(self._others_write_handler)
        self._others_read_btn.handler_block(self._others_read_handler)
        self._others_execute_btn.handler_block(self._others_execute_handler)

    def _unblock_all_handlers(self):
        self._owner_write_btn.handler_unblock(self._owner_write_handler)
        self._owner_read_btn.handler_unblock(self._owner_read_handler)
        self._owner_execute_btn.handler_unblock(self._owner_execute_handler)
        self._group_write_btn.handler_unblock(self._group_write_handler)
        self._group_read_btn.handler_unblock(self._group_read_handler)
        self._group_execute_btn.handler_unblock(self._group_execute_handler)
        self._others_write_btn.handler_unblock(self._others_write_handler)
        self._others_read_btn.handler_unblock(self._others_read_handler)
        self._others_execute_btn.handler_unblock(self._others_execute_handler)

    def _on_symbolic_entry_changed(self, user_date: GObject.GPointer):
        self._symbolic_row.remove_css_class("border-red")

        self._block_all_handlers()
        self._uncheck_btns()
        self._unblock_all_handlers()

        if len(self._symbolic_row.get_text()) == 9:
            if not Utils.is_symbolic_chmod(self._symbolic_row.get_text()):
                self._symbolic_row.add_css_class("border-red")
                self._block_all_handlers()
                self._numeric_row.set_text("000")
                self._unblock_all_handlers()
                self._toast.add_toast(self._invalid_toast)
                return
            else:
                symbolic = list(self._symbolic_row.get_text())

                # Owner
                if symbolic[0] != '-':
                    self._block_all_handlers()
                    self._owner_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[1] != '-':
                    self._block_all_handlers()
                    self._owner_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[2] != '-':
                    self._block_all_handlers()
                    self._owner_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Group
                if symbolic[3] != '-':
                    self._block_all_handlers()
                    self._group_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[4] != '-':
                    self._block_all_handlers()
                    self._group_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[5] != '-':
                    self._block_all_handlers()
                    self._group_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Others
                if symbolic[6] != '-':
                    self._block_all_handlers()
                    self._others_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[7] != '-':
                    self._block_all_handlers()
                    self._others_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[8] != '-':
                    self._block_all_handlers()
                    self._others_execute_btn.set_active(True)
                    self._unblock_all_handlers()
        else:
            self._symbolic_row.add_css_class("border-red")
