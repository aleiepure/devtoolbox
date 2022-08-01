# json2yaml_utility.py
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


import json
from gettext import gettext as _
import warnings
from gi.repository import Gtk, Adw, Gdk
from ruamel import yaml


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/json2yaml_utility.ui")
class Json2YamlUtility(Adw.Bin):
    __gtype_name__ = "Json2YamlUtility"

    indents_combo = Gtk.Template.Child()
    direction_combo = Gtk.Template.Child()
    indents_combo_items = Gtk.Template.Child()
    direction_combo_items = Gtk.Template.Child()
    starred_btn = Gtk.Template.Child()
    convert_btn = Gtk.Template.Child()
    open_btn = Gtk.Template.Child()
    paste_btn = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()
    input_textview = Gtk.Template.Child()
    output_textview = Gtk.Template.Child()
    toast = Gtk.Template.Child()

    def __init__(self):
        super().__init__()
        # TODO: add favorites logic to button
        # self.starred_btn.set_icon_name("non-starred")

        # Populate indents combo box
        for i in range(2, 10, 2):
            self.indents_combo_items.append(f"{i} {_('Spaces')}")

        # Connect button signals
        self.convert_btn.connect("clicked", self.on_convert_clicked)
        self.open_btn.connect("clicked", self.on_open_clicked)
        self.paste_btn.connect("clicked", self.on_paste_clicked)
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        self.copy_btn.connect("clicked", self.on_copy_clicked)

    def on_convert_clicked(self, widget):
        input_buffer = self.input_textview.get_buffer()
        output_buffer = self.output_textview.get_buffer()
        input_text = input_buffer.get_text(
            input_buffer.get_start_iter(), input_buffer.get_end_iter(), False)
        
        if self.direction_combo.get_selected() == 0:
            try:
                output_buffer.set_text(yaml.dump(
                    json.loads(input_text),
                    indent=2*self.indents_combo.get_selected()+2
                ))
            except:
                self.toast.add_toast(Adw.Toast(title=_("Input is not a valid JSON file")))
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                try:
                    output_buffer.set_text(json.dumps(
                        yaml.load(input_text),
                        indent=2*self.indents_combo.get_selected()+2,
                        ensure_ascii=False
                    ))
                except:
                    self.toast.add_toast(Adw.Toast(title=_("Input is not a valid YAML file")))

    def on_open_clicked(self, widget):

        self._native = Gtk.FileChooserNative(
            title="Open File",
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel"
        )

        extensions = ["json", "yaml", "yml"]
        filter = Gtk.FileFilter()
        for f in extensions:
            filter.add_suffix(f)
        filter.set_name(f"{_('JSON & YAML Files')}")
        self._native.add_filter(filter)

        # Connect the "response" signal
        self._native.connect("response", self.on_open_response)
        self._native.show()

    def on_open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.open_file(dialog.get_file())

        # Delete filechooser
        self._native = None

    def open_file(self, file):
        file.load_contents_async(None, self.open_file_complete)

    def open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)
        if not contents[0]:
            path = file.peek_path()
            print(f"Unable to open {path}: {contents[1]}")
            return

        try:
            text = contents[1].decode('utf-8')
        except UnicodeError as err:
            path = file.peek_path()
            print(
                f"Unable to load the contents of {path}: the file is not encoded with UTF-8")
            return

        buffer = self.input_textview.get_buffer()
        buffer.set_text(text)
        buffer.place_cursor(buffer.get_start_iter())

    def on_paste_clicked(self, widget):
        buffer = self.input_textview.get_buffer()
        display = Gdk.Display.get_default()
        clipboard = Gdk.Display.get_clipboard(display)
        buffer.paste_clipboard(clipboard, None, True)

    def on_clear_clicked(self, widget):
        buffer = self.input_textview.get_buffer()
        buffer.set_text("")
        buffer = self.output_textview.get_buffer()
        buffer.set_text("")

    def on_copy_clicked(self, widget):
        buffer = self.output_textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)
        display = Gdk.Display.get_default()
        clipboard = Gdk.Display.get_clipboard(display)
        clipboard.set(text)
