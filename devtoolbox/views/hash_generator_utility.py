# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio
from gettext import gettext as _

from devtoolbox.services.hash_generator import HashGenerator


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/hash_generator_utility.ui")
class HashGeneratorUtility(Adw.Bin):
    __gtype_name__ = "HashGeneratorUtility"

    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _uppercase_switch = Gtk.Template.Child()
    _text_image_file_area = Gtk.Template.Child()
    _md5 = Gtk.Template.Child()
    _sha1 = Gtk.Template.Child()
    _sha256 = Gtk.Template.Child()
    _sha512 = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Signals
        self._title.connect("added-favorite", self._on_added_favorite)
        self._title.connect("removed-favorite", self._on_removed_favorite)
        self._uppercase_switch.connect("notify::active", self._on_uppercase_state_changed)
        self._text_image_file_area.connect("error", self._on_error)
        self._text_image_file_area.connect("text-changed", self._on_input_changed)
        self._text_image_file_area.connect("image-loaded", self._on_input_changed)
        self._text_image_file_area.connect("file-loaded", self._on_input_changed)
        self._text_image_file_area.connect("view-cleared", self._on_view_cleared)

    def _on_added_favorite(self, widget):
        self._toast.add_toast(Adw.Toast(title="Added to favorites!"))

    def _on_removed_favorite(self, widget):
        self._toast.add_toast(Adw.Toast(title="Removed from favorites!"))


    def _on_uppercase_state_changed(self, state, data):
        self.generate_hash_async(self._done_hashing)

    def _on_input_changed(self, widget):
        self.generate_hash_async(self._done_hashing)

    def _on_error(self, error):
        self._toast.add_toast(Adw.Toast(title=f"Error: {error}"))

    def _done_hashing(self, source_object, result, data):
        outcome = self._generate_hash_finish(result)
        md5, sha1, sha256, sha512 = outcome
        if not self.cancellable.is_cancelled() and outcome != -1:
            self._md5.set_text(md5)
            self._sha1.set_text(sha1)
            self._sha256.set_text(sha256)
            self._sha512.set_text(sha512)
        self._text_image_file_area.set_loading_visible(False)
    
    def _on_view_cleared(self, widget):
        self.cancellable.cancel()
        self._md5.set_text("")
        self._sha1.set_text("")
        self._sha256.set_text("")
        self._sha512.set_text("")

    def generate_hash_async(self, callback):
        self._text_image_file_area.set_loading_visible(True)
        self.cancellable = Gio.Cancellable()
        self.task = Gio.Task.new(self, None, callback, self.cancellable)
        self.task.set_return_on_cancel(True)
        self.task.run_in_thread(self._generate_hash_thread_callback)

    def _generate_hash_finish(self, result):
        if not Gio.Task.is_valid(result, self):
            return -1
        return result.propagate_value().value
    
    def _generate_hash_thread_callback(self, task, source_objcet, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._get_hashes()
        task.return_value(outcome)
        
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
        
