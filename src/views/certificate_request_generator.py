# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gio, GObject, Gdk
from typing import List
import subprocess


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/certificate_request_generator.ui')
class CertificateRequestGeneratorView(Adw.Bin):
    __gtype_name__ = "CertificateRequestGeneratorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _preferences_group = Gtk.Template.Child()
    _create_csr_btn = Gtk.Template.Child()
    _common_name_entry = Gtk.Template.Child()
    _country_name_entry = Gtk.Template.Child()
    _state_entry = Gtk.Template.Child()
    _locality_entry = Gtk.Template.Child()
    _organization_entry = Gtk.Template.Child()
    _organization_unit_entry = Gtk.Template.Child()
    _password_entry = Gtk.Template.Child()
    _key_type_selector = Gtk.Template.Child()
    _key_open_row = Gtk.Template.Child()
    _key_open_path = Gtk.Template.Child()
    _key_open_btn = Gtk.Template.Child()
    _key_size_selector = Gtk.Template.Child()
    _key_save_row = Gtk.Template.Child()
    _key_save_path = Gtk.Template.Child()
    _key_save_btn = Gtk.Template.Child()

    _saved_toast = Adw.Toast(priority=Adw.ToastPriority.HIGH, button_label=_("Open folder"))

    def __init__(self):
        super().__init__()

        # Fix style
        self._preferences_group.get_first_child().get_last_child().get_first_child().remove_css_class("boxed-list")
        self._preferences_group.get_first_child().get_last_child().get_first_child().get_row_at_index(0).add_css_class("fake-action-row-top")
        i = 1
        while(self._preferences_group.get_first_child().get_last_child().get_first_child().get_row_at_index(i) != None):
            self._preferences_group.get_first_child().get_last_child().get_first_child().get_row_at_index(i).add_css_class("fake-action-row-middle")
            i += 1

        # Signals
        self._key_open_btn.connect("clicked", self._on_key_open_clicked)
        self._key_save_btn.connect("clicked", self._on_key_save_clicked)
        self._create_csr_btn.connect("clicked", self._on_create_csr_clicked)
        self._common_name_entry.connect("changed", self._on_entry_changed)
        self._saved_toast.connect("button-clicked", self._on_toast_btn_clicked)

    def _on_key_open_clicked(self, user_data: GObject.GPointer):

        # Disable button
        self._key_open_btn.set_sensitive(False)
        self._key_open_row.remove_css_class("border-red")

        # Create a file chooser
        app = Gio.Application.get_default()
        window = app.get_active_window()
        self._native = Gtk.FileChooserNative(
            transient_for=window,
            title=_("Open Key File"),
            action=Gtk.FileChooserAction.OPEN,
            accept_label=_("Open"),
            cancel_label=_("Cancel")
        )

        # Set filters
        file_filter = Gtk.FileFilter()
        file_filter.add_suffix("*")
        file_filter.set_name(_("All Files"))
        self._native.add_filter(file_filter)

        # Signals and show dialog
        self._native.connect("response", self._on_open_response)
        self._native.show()

    def _on_open_response(self, dialog: Gtk.NativeDialog, response: int):

        # Show path
        if response == Gtk.ResponseType.ACCEPT:
            self._key_open_path.set_label(dialog.get_file().get_path())
        self._native = None

        # Re-enable open button
        self._key_open_btn.set_sensitive(True)

    def _field_checks(self):

        has_errors = False

        if len(self._common_name_entry.get_text()) <= 0:
            self._common_name_entry.add_css_class("border-red")
            has_errors = True

        if (self._key_type_selector.get_right_btn_active() and len(self._key_open_path.get_label()) <= 0):
            self._key_open_row.add_css_class("border-red")
            has_errors = True

        if (self._key_type_selector.get_left_btn_active() and len(self._key_save_path.get_label()) <= 0):
            self._key_save_row.add_css_class("border-red")
            has_errors = True

        return has_errors

    def _on_create_csr_clicked(self, user_data: GObject.GPointer):

        # Check for mandatory fields
        if not self._field_checks():

            # Determine key type
            if self._key_type_selector.get_left_btn_active():
                if self._key_size_selector.get_left_btn_active():
                    key_args = ["-newkey", "rsa:2048"]
                else:
                    key_args = ["-newkey", "rsa:4096"]
            else:
                key_args = ["-key", self._key_open_path.get_label()]

            # Save path
            app = Gio.Application.get_default()
            window = app.get_active_window()
            self._file_dialog = Gtk.FileDialog(
                modal=True,
                title=_("Save file as"),
                accept_label=_("Save"),
                initial_name=self._common_name_entry.get_text() + ".csr"
            )
            self._file_dialog.save(window, None, self._on_save_complete, key_args)

    def _on_save_complete(self, source: GObject.Object, result: Gio.AsyncResult, user_data: List = None):

        # Get user selected file
        save_file = source.save_finish(result)

        # Build OpenSSL command
        command = []
        command.append("openssl")
        command.append("req")
        command.append("-new")
        command.extend(user_data)
        command.append("-out")
        command.append(save_file.peek_path())

        if self._key_type_selector.get_left_btn_active():
            command.append("-keyout")
            command.append(self._key_save_path.get_label())


        if len(self._password_entry.get_text()) > 0:
            command.append("-passin")
            command.append(f"pass:{self._password_entry.get_text()}")
        else:
            command.append("-noenc")

        command.append("-subj")

        # Build subject string
        subject = ""
        if len(self._common_name_entry.get_text()) > 0:
            subject += "/CN=" + self._common_name_entry.get_text()
        if len(self._country_name_entry.get_text()) > 0:
            subject += "/C=" + self._country_name_entry.get_text()
        if len(self._state_entry.get_text()) > 0:
            subject += "/ST=" + self._state_entry.get_text()
        if len(self._locality_entry.get_text()) > 0:
            subject += "/L=" + self._locality_entry.get_text()
        if len(self._organization_entry.get_text()) > 0:
            subject += "/O=" + self._organization_entry.get_text()
        if len(self._organization_unit_entry.get_text()) > 0:
            subject += "/OU=" + self._organization_unit_entry.get_text()
        command.append(subject)

        # Call to OpenSSL
        openssl = subprocess.run(command, capture_output=True)
        if openssl.returncode == 0:
            self._saved_toast.set_title(_("Successfully saved as {save_path}").format(save_path=save_file.peek_path()))
            self._toast.add_toast(self._saved_toast)
        else:
            self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(error=openssl.stderr.decode().strip()), priority=Adw.ToastPriority.HIGH))
            if openssl.stderr.decode().strip().startswith("Could not read private key from "):
                self._key_open_row.add_css_class("border-red")

    def _on_entry_changed(self, user_data: GObject.GPointer):
        self._common_name_entry.remove_css_class("border-red")

    def _on_key_save_clicked(self, user_data: GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        self._file_dialog = Gtk.FileDialog(
            modal=True,
            title=_("Save key as"),
            accept_label=_("Save"),
            initial_name=self._common_name_entry.get_text() + ".key"
        )
        self._file_dialog.save(window, None, self._on_key_save_complete, None)

    def _on_key_save_complete(self, source: GObject.Object, result: Gio.AsyncResult, user_data: List = None):
        save_file = source.save_finish(result)
        self._key_save_path.set_label(save_file.peek_path())

    def _on_toast_btn_clicked(self, user_data:GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        full_msg = self._saved_toast.get_title()
        full_path = full_msg[full_msg.index("/"):len(full_msg)]
        folder_path = full_path[:full_path.rindex("/")]
        Gtk.show_uri(window, "file://" + folder_path, Gdk.CURRENT_TIME)
