# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GtkSource, Gdk
from gettext import gettext as _


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/file_viewer.ui')
class FileViewer(Adw.Bin):
    __gtype_name__ = 'FileViewer'

    # Template elements
    _file_path_lbl = Gtk.Template.Child()
    _file_size_lbl = Gtk.Template.Child()

    # Properties
    file_path = GObject.Property(type=str, default="")
    file_size = GObject.Property(type=str, default="")

    def __init__(self):
        super().__init__()

        # Property binding
        self.bind_property("file_path", self._file_path_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("file_size", self._file_size_lbl, "label", GObject.BindingFlags.SYNC_CREATE)

    def get_file_path(self) -> str:
        return self.file_path

    def set_file_path(self, file_path:str):
        self.file_path = file_path

    def get_file_size(self) -> str:
        return self.file_size

    def set_file_size(self, file_size:str):
        self.file_size = file_size
