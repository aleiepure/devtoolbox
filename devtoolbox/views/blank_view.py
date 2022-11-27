# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

# TEMPLATE ONLY, NOT TO BE USED

from gi.repository import Adw, Gtk
from gettext import gettext as _


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/file_name.ui")
class BlankView(Adw.Bin):
    __gtype_name__ = "BlankView"

    # UI components
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._title.connect("added-favorite", self._on_added_favorite)
        self._title.connect("removed-favorite", self._on_removed_favorite)
    
    def _on_added_favorite(self, widget):
        self._toast.add_toast(Adw.Toast(title="Added to favorites!"))

    def _on_removed_favorite(self, widget):
        self._toast.add_toast(Adw.Toast(title="Removed from favorites!"))

    def _on_error(self, error):
        self._toast.add_toast(Adw.Toast(title=f"Error: {error}"))