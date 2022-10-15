# text_area.py
#
# Copyright 2022 Alessandro Iepure
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Adw, GObject, Gdk
from gettext import gettext as _


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/textfield_action_row.ui')
class TextFieldActionRow(Adw.ActionRow):
    __gtype_name__ = "TextfieldActionRow"

    _text = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()
    _spacer = Gtk.Template.Child()

    # Custom properties
    editable = GObject.Property(type=bool, default=True)
    show_copy_btn = GObject.Property(type=bool, default=False)
    show_paste_btn = GObject.Property(type=bool, default=False)
    show_clear_btn = GObject.Property(type=bool, default=False)

    # Custom signals
    __gsignals__ = {
        "text-changed": (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self):
        super().__init__()

        if self.show_clear_btn or self.show_copy_btn or self.show_paste_btn:
            self._spacer.set_visible(True)
        else:
            self._spacer.set_visible(False)

        # Property binding
        self.bind_property("show-copy-btn", self._copy_btn, "visible",
                           GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-paste-btn", self._paste_btn, "visible",
                           GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-clear-btn", self._clear_btn, "visible",
                           GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("editable", self._text, "editable",
                           GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-copy-btn", self._spacer,
                           "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-clear-btn", self._spacer,
                           "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-paste-btn", self._spacer,
                           "visible", GObject.BindingFlags.SYNC_CREATE)

        # Signals
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._clear_btn.connect("clicked", self._on_clear_clicked)
        self._text.connect("notify::text", self._on_text_changed)

    def _on_copy_clicked(self, data):
        text = self._text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)
    
    def _on_paste_clicked(self, data):
        self._text.emit("paste-clipboard")
    
    def _on_clear_clicked(self, data):
        self._text.set_text("")
    
    def _on_text_changed(self, widget, data):
        self.emit("text-changed")

    def set_text(self, text):
        self._text.get_buffer().set_text(text, -1)