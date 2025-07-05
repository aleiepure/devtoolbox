# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject

from ..utils import Utils
from gettext import gettext as _


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
    _special_setuid_btn = Gtk.Template.Child()
    _special_setgid_btn = Gtk.Template.Child()
    _special_sticky_btn = Gtk.Template.Child()
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
        self._special_setuid_btn_handler = self._special_setuid_btn.connect("toggled", self._on_button_toggled)
        self._special_setgid_btn_handler = self._special_setgid_btn.connect("toggled", self._on_button_toggled)
        self._special_sticky_btn_handler = self._special_sticky_btn.connect("toggled", self._on_button_toggled)
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
        if self._special_setuid_btn.get_active():
            value += 4000
            symbolic[2] = "s" if self._owner_execute_btn.get_active() else "S"
        if self._special_setgid_btn.get_active():
            value += 2000
            symbolic[5] = "s" if self._group_execute_btn.get_active() else "S"
        if self._special_sticky_btn.get_active():
            value += 1000
            symbolic[8] = "t" if self._others_execute_btn.get_active() else "T"

        self._block_all_handlers()

        self._numeric_row.set_text(f"{value:04d}" if len(str(value)) > 3 else f"{value:03d}")
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
        self._special_setuid_btn.set_active(False)
        self._special_setgid_btn.set_active(False)
        self._special_sticky_btn.set_active(False)

    def _on_numeric_entry_changed(self, user_date: GObject.GPointer):
        self._numeric_row.remove_css_class("border-red")

        self._block_all_handlers()
        self._uncheck_btns()
        self._unblock_all_handlers()

        if 3 <= len(self._numeric_row.get_text()) <= 4:
            if not Utils.is_numeric_chmod(int(self._numeric_row.get_text())):
                self._numeric_row.add_css_class("border-red")
                self._block_all_handlers()
                self._symbolic_row.set_text("")
                self._unblock_all_handlers()
                self._toast.add_toast(self._invalid_toast)
                return
            else:
                symbolic = list("---------")
                l = list(self._numeric_row.get_text())
                special = int(l.pop(0)) if len(l) > 3 else 0
                owner = int(l[0])
                group = int(l[1])
                others = int(l[2])

                # Owner
                if owner - 4 >= 0:
                    owner -= 4
                    self._block_all_handlers()
                    symbolic[0] = "r"
                    self._owner_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if owner - 2 >= 0:
                    owner -= 2
                    self._block_all_handlers()
                    symbolic[1] = "w"
                    self._owner_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if owner - 1 >= 0:
                    owner -= 1
                    self._block_all_handlers()
                    symbolic[2] = "x"
                    self._owner_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Group
                if group - 4 >= 0:
                    group -= 4
                    self._block_all_handlers()
                    symbolic[3] = "r"
                    self._group_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if group - 2 >= 0:
                    group -= 2
                    self._block_all_handlers()
                    symbolic[4] = "w"
                    self._group_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if group - 1 >= 0:
                    group -= 1
                    self._block_all_handlers()
                    symbolic[5] = "x"
                    self._group_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Others
                if others - 4 >= 0:
                    others -= 4
                    self._block_all_handlers()
                    symbolic[6] = "r"
                    self._others_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if others - 2 >= 0:
                    others -= 2
                    self._block_all_handlers()
                    symbolic[7] = "w"
                    self._others_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if others - 1 >= 0:
                    others -= 1
                    self._block_all_handlers()
                    symbolic[8] = "x"
                    self._others_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Special
                if special - 4 >= 0:
                    special -= 4
                    self._block_all_handlers()
                    symbolic[2] = "s" if symbolic[2] == "x" else "S"
                    self._special_setuid_btn.set_active(True)
                    self._unblock_all_handlers()
                if special - 2 >= 0:
                    special -= 2
                    self._block_all_handlers()
                    symbolic[5] = "s" if symbolic[5] == "x" else "S"
                    self._special_setgid_btn.set_active(True)
                    self._unblock_all_handlers()
                if special - 1 >= 0:
                    special -= 1
                    self._block_all_handlers()
                    symbolic[8] = "t" if symbolic[8] == "x" else "T"
                    self._special_sticky_btn.set_active(True)
                    self._unblock_all_handlers()

                self._block_all_handlers()
                self._symbolic_row.set_text("".join(symbolic))
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
        self._special_setuid_btn.handler_block(self._special_setuid_btn_handler)
        self._special_setgid_btn.handler_block(self._special_setgid_btn_handler)
        self._special_sticky_btn.handler_block(self._special_sticky_btn_handler)
        self._numeric_row.handler_block(self._numeric_handler)
        self._symbolic_row.handler_block(self._symbolic_handler)

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
        self._special_setuid_btn.handler_unblock(self._special_setuid_btn_handler)
        self._special_setgid_btn.handler_unblock(self._special_setgid_btn_handler)
        self._special_sticky_btn.handler_unblock(self._special_sticky_btn_handler)
        self._numeric_row.handler_unblock(self._numeric_handler)
        self._symbolic_row.handler_unblock(self._symbolic_handler)

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
                value = 0

                # Owner
                if symbolic[0] != '-':
                    self._block_all_handlers()
                    value += 400
                    self._owner_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[1] != '-':
                    self._block_all_handlers()
                    value += 200
                    self._owner_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[2] != '-':
                    self._block_all_handlers()
                    if symbolic[2] == 's':
                        value += 4100
                        self._owner_execute_btn.set_active(True)
                        self._special_setuid_btn.set_active(True)
                    elif symbolic[2] == 'S':
                        value += 4000
                        self._special_setuid_btn.set_active(True)
                    else:
                        value += 100
                        self._owner_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Group
                if symbolic[3] != '-':
                    self._block_all_handlers()
                    value += 40
                    self._group_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[4] != '-':
                    self._block_all_handlers()
                    value += 20
                    self._group_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[5] != '-':
                    self._block_all_handlers()
                    if symbolic[5] == 's':
                        value += 2010
                        self._group_execute_btn.set_active(True)
                        self._special_setgid_btn.set_active(True)
                    elif symbolic[5] == 'S':
                        value += 2000
                        self._special_setgid_btn.set_active(True)
                    else:
                        value += 10
                        self._group_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                # Others
                if symbolic[6] != '-':
                    self._block_all_handlers()
                    value += 4
                    self._others_read_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[7] != '-':
                    value += 2
                    self._block_all_handlers()
                    self._others_write_btn.set_active(True)
                    self._unblock_all_handlers()
                if symbolic[8] != '-':
                    self._block_all_handlers()
                    if symbolic[8] == 't':
                        value += 1001
                        self._others_execute_btn.set_active(True)
                        self._special_sticky_btn.set_active(True)
                    elif symbolic[8] == 'T':
                        value += 1000
                        self._special_sticky_btn.set_active(True)
                    else:
                        value += 1
                        self._others_execute_btn.set_active(True)
                    self._unblock_all_handlers()

                self._block_all_handlers()
                self._numeric_row.set_text(f"{value:04d}" if len(str(value)) > 3 else f"{value:03d}")
                self._unblock_all_handlers()
        else:
            self._symbolic_row.add_css_class("border-red")
