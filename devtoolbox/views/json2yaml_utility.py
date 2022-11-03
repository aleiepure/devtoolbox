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

from ..services.json2yaml import JSON2YAML
from gettext import gettext as _
from gi.repository import Gtk, Adw, Gdk, Gio


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/json2yaml_utility.ui")
class Json2YamlUtility(Adw.Bin):
    __gtype_name__ = "Json2YamlUtility"

    toast = Gtk.Template.Child()
    direction_toggle = Gtk.Template.Child()
    indents_spinner = Gtk.Template.Child()
    input_area = Gtk.Template.Child()
    output_area = Gtk.Template.Child()

    # True: JSON to YAML, False: YAML to JSON
    direction = True

    def __init__(self):
        super().__init__()

        # Signals
        self.direction_toggle.connect("toggled", self.on_direction_toggled)
        self.indents_spinner.connect("value-changed", self.on_indents_changed)
        self.input_area.connect("text-changed", self.on_text_changed)
        self.input_area.connect("text-loaded", self.on_loaded)
        self.input_area.connect("error", self.on_error)
        self.input_area.connect("view-cleared", self.on_view_cleared)
        self.output_area.connect("error", self.on_error)

    def on_view_cleared(self, data):
        self.output_area.set_text("")
        
    def on_direction_toggled(self, data):
        self.direction = self.direction_toggle.get_active()
        self._convert()

    def on_indents_changed(self, data):
        self._convert()

    def on_text_changed(self, data):
        self._convert()

    def on_error(self, error):
        self.toast.add_toast(Adw.Toast(title=f"Error: {error}"))
    
    def on_loaded(self, data):
        self._convert()


    def _convert(self):

        self.input_area.remove_css_class("border-red")

        input_text = self.input_area.get_text()
        indents = int(self.indents_spinner.get_value())

        # True: JSON to YAML, False: YAML to JSON
        if self.direction:
            if len(input_text) > 0 and JSON2YAML.is_json(input_text):
                self.output_area.set_text(JSON2YAML.to_yaml(input_text, indents))
            else:
                self.input_area.add_css_class("border-red")
        else:
            if len(input_text) > 0 and JSON2YAML.is_yaml(input_text):
                self.output_area.set_text(JSON2YAML.to_json(input_text, indents))
            else:
                self.input_area.add_css_class("border-red")
