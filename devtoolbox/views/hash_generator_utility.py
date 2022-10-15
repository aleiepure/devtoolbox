# hash_generator_utility.py
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

import threading
from gi.repository import Adw, Gtk, Gio, Gdk, GLib, GObject
from gettext import gettext as _

from devtoolbox.services.hash_generator import HashGenerator
from devtoolbox.services.number_base import Bases, NumberBase
from devtoolbox.utils import Utils


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/hash_generator_utility.ui")
class HashGeneratorUtility(Adw.Bin):
    __gtype_name__ = "HashGeneratorUtility"

    _toast = Gtk.Template.Child()
    _uppercase_switch = Gtk.Template.Child()
    _text_image_file_area = Gtk.Template.Child()
    _md5 = Gtk.Template.Child()
    _sha1 = Gtk.Template.Child()
    _sha256 = Gtk.Template.Child()
    _sha512 = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Signals
        self._uppercase_switch.connect("notify::active", self._on_uppercase_state_changed)
        self._text_image_file_area.connect("error", self._on_error)
        self._text_image_file_area.connect("text-changed", self._on_input_changed)
        self._text_image_file_area.connect("image-loaded", self._on_input_changed)
        self._text_image_file_area.connect("file-loaded", self._on_input_changed)
        self._text_image_file_area.connect("view-cleared", self._on_view_cleared)

    def _on_uppercase_state_changed(self, state, data):
        self.generate_hash_async(self._done_hashing)

    def _on_input_changed(self, widget):
        self.generate_hash_async(self._done_hashing)

    def _on_error(self, error):
        self._toast.add_toast(Adw.Toast(title=f"Error: {error}"))

    def _done_hashing(self, return_val):
        md5, sha1, sha256, sha512 = return_val
        self._md5.set_text(md5)
        self._sha1.set_text(sha1)
        self._sha256.set_text(sha256)
        self._sha512.set_text(sha512)
    
    def _on_view_cleared(self, widget):
        self._md5.set_text("")
        self._sha1.set_text("")
        self._sha256.set_text("")
        self._sha512.set_text("")

    def generate_hash_async(self, callback):
        self._text_image_file_area.set_loading_visible(True)

        def _thread_run():
            hashes = self._get_hashes()
            GObject.idle_add(_cleanup, hashes)
        
        def _cleanup(return_val):
            self._text_image_file_area.set_loading_visible(False)
            t.join()
            callback(return_val)

        t = threading.Thread(group=None, target=_thread_run)
        t.start()
        
    def _get_hashes(self):        
        uppercase = self._uppercase_switch.get_active()

        if self._text_image_file_area.get_visible_view() == "text":
            text = self._text_image_file_area.get_text()
            if len(text)>0:
                md5 = HashGenerator.to_md5(text)
                sha1 = HashGenerator.to_sha1(text)
                sha256 = HashGenerator.to_sha256(text)
                sha512 = HashGenerator.to_sha512(text)
            else:
                return "", "", "", ""
        else:
            file_path = self._text_image_file_area.get_file_path()
            md5 = HashGenerator.file_to_md5(file_path)
            sha1 = HashGenerator.file_to_sha1(file_path)
            sha256 = HashGenerator.file_to_sha256(file_path)
            sha512 = HashGenerator.file_to_sha512(file_path)

        if uppercase == True:
            md5 = md5.upper()
            sha1 = sha1.upper()
            sha256 = sha256.upper()
            sha512 = sha512.upper()

        return md5, sha1, sha256, sha512
        
