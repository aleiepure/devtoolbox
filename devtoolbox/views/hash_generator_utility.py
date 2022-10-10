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

    toast = Gtk.Template.Child()
    uppercase_switch = Gtk.Template.Child()
    text_image_file_area = Gtk.Template.Child()

    md5_text = Gtk.Template.Child()
    md5_copy_btn = Gtk.Template.Child()
    sha1_text = Gtk.Template.Child()
    sha1_copy_btn = Gtk.Template.Child()
    sha256_text = Gtk.Template.Child()
    sha256_copy_btn = Gtk.Template.Child()
    sha512_text = Gtk.Template.Child()
    sha512_copy_btn = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Signals
        self.uppercase_switch.connect(
            "notify::active", self.on_uppercase_state_changed)
        self.text_image_file_area.connect("error", self.on_error)
        self.text_image_file_area.connect("text-changed", self.on_input_changed)
        self.text_image_file_area.connect("image-loaded", self.on_input_changed)
        self.text_image_file_area.connect("file-loaded", self.on_input_changed)
        self.text_image_file_area.connect("view-cleared", self.on_view_cleared)
        self.md5_copy_btn.connect("clicked", self.on_md5_copy_clicked)
        self.sha1_copy_btn.connect("clicked", self.on_sha1_copy_clicked)
        self.sha256_copy_btn.connect("clicked", self.on_sha256_copy_clicked)
        self.sha512_copy_btn.connect("clicked", self.on_sha512_copy_clicked)

    def on_uppercase_state_changed(self, state, data):
        self.generate_hash_async(self.done_hashing)

    def on_big_file(self, widget, size):
        self.toast.add_toast(Adw.Toast(
            title=f"File too large to show contents ({str(round(size / (1024 * 1024 * 1024), 2))} GB)"))

    def on_error(self, error):
        self.toast.add_toast(Adw.Toast(title=f"Error: {error}"))
    
    def on_input_changed(self, widget):
        self.generate_hash_async(self.done_hashing)

    def done_hashing(self, return_val):
        md5, sha1, sha256, sha512 = return_val
        self.md5_text.get_buffer().set_text(md5, -1)
        self.sha1_text.get_buffer().set_text(sha1, -1)
        self.sha256_text.get_buffer().set_text(sha256, -1)
        self.sha512_text.get_buffer().set_text(sha512, -1)
    
    def on_view_cleared(self, widget):
        self.md5_text.set_text("")
        self.sha1_text.set_text("")
        self.sha256_text.set_text("")
        self.sha512_text.set_text("")

    def on_md5_copy_clicked(self, data):
        text = self.md5_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_sha1_copy_clicked(self, data):
        text = self.sha1_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_sha256_copy_clicked(self, data):
        text = self.sha256_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def on_sha512_copy_clicked(self, data):
        text = self.sha512_text.get_buffer().get_text()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def generate_hash_async(self, callback):
        self.text_image_file_area.set_loading_visible(True)

        def thread_run():
            hashes = self.generate_hash()
            GObject.idle_add(cleanup, hashes)
        
        def cleanup(return_val):
            self.text_image_file_area.set_loading_visible(False)
            t.join()
            callback(return_val)

        t = threading.Thread(group=None, target=thread_run)
        t.start()
        

    def generate_hash(self):        
        uppercase = self.uppercase_switch.get_active()

        if self.text_image_file_area.get_visible_view() == "text":
            text = self.text_image_file_area.get_text()
            md5 = HashGenerator.to_md5(text)
            sha1 = HashGenerator.to_sha1(text)
            sha256 = HashGenerator.to_sha256(text)
            sha512 = HashGenerator.to_sha512(text)
        else:
            file_path = self.text_image_file_area.get_file_path()
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
        
