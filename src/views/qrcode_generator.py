# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GObject, GLib, Gdk, GdkPixbuf
import qrcode
from qrcode.image.pure import PyPNGImage
import qrcode.image.svg
from gettext import gettext as _


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/qrcode_generator.ui")
class QRCodeGeneratorView(Adw.Bin):
    __gtype_name__ = "QRCodeGeneratorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _type_combo = Gtk.Template.Child()
    _text_entry = Gtk.Template.Child()
    _wifi_ssid_entry = Gtk.Template.Child()
    _wifi_encryption_combo = Gtk.Template.Child()
    _wifi_password_entry = Gtk.Template.Child()
    _contact_last_name_entry = Gtk.Template.Child()
    _contact_first_name_entry = Gtk.Template.Child()
    _contact_phone_entry = Gtk.Template.Child()
    _contact_email_entry = Gtk.Template.Child()
    _contact_birthday_row = Gtk.Template.Child()
    _contact_birthday_btn = Gtk.Template.Child()
    _contact_birthday_not_set_btn = Gtk.Template.Child()
    _contact_birthday_calendar_btn = Gtk.Template.Child()
    _contact_birthday_calendar = Gtk.Template.Child()
    _contact_url_entry = Gtk.Template.Child()
    _contact_address_row = Gtk.Template.Child()
    _contact_address_street_entry = Gtk.Template.Child()
    _contact_address_city_entry = Gtk.Template.Child()
    _contact_address_state_entry = Gtk.Template.Child()
    _contact_address_zip_entry = Gtk.Template.Child()
    _contact_address_country_entry = Gtk.Template.Child()
    _qrcode_area = Gtk.Template.Child()

    _saved_toast = Adw.Toast(
        priority=Adw.ToastPriority.HIGH, button_label=_("Open Image"))

    def __init__(self):
        super().__init__()

        self._update_visible_rows()

        # Signals
        self._type_combo.connect(
            "notify::selected", self._on_type_combo_changed)
        self._contact_birthday_not_set_btn.connect(
            "toggled", self._on_birthday_btn_toggled)
        self._contact_birthday_calendar.connect(
            "day-selected", self._on_birthday_calendar_selected)
        self._qrcode_area.connect("save-clicked", self._on_save_clicked)
        self._contact_first_name_entry.connect(
            "changed", self._on_first_name_changed)
        self._contact_last_name_entry.connect(
            "changed", self._on_last_name_changed)
        self._qrcode_area.connect("view-clicked", self._on_view_clicked)
        self._qrcode_area.connect("action-clicked", self._on_generate_clicked)
        self._saved_toast.connect("button-clicked", self._on_toast_btn_clicked)

    def _on_type_combo_changed(self, pspec: GObject.ParamSpec, user_data: GObject.GPointer):
        self._update_visible_rows()

    def _on_birthday_btn_toggled(self, user_data: GObject.GPointer):
        if self._contact_birthday_not_set_btn.get_active():
            self._contact_birthday_btn.set_label(_("Not Set"))
        else:
            self._contact_birthday_btn.set_label(
                self._contact_birthday_calendar.get_date().format("%x"))

    def _on_birthday_calendar_selected(self, user_data: GObject.GPointer):
        self._contact_birthday_calendar_btn.set_active(True)

    def _update_visible_rows(self):
        self._hide_all_rows()
        match self._type_combo.get_selected():
            case 0:
                self._text_entry.set_visible(True)
            case 1:
                self._wifi_ssid_entry.set_visible(True)
                self._wifi_encryption_combo.set_visible(True)
                self._wifi_password_entry.set_visible(True)
            case 2:
                self._contact_first_name_entry.set_visible(True)
                self._contact_last_name_entry.set_visible(True)
                self._contact_phone_entry.set_visible(True)
                self._contact_email_entry.set_visible(True)
                self._contact_birthday_row.set_visible(True)
                self._contact_url_entry.set_visible(True)
                self._contact_address_row.set_visible(True)

    def _hide_all_rows(self):
        self._text_entry.set_visible(False)
        self._wifi_ssid_entry.set_visible(False)
        self._wifi_encryption_combo.set_visible(False)
        self._wifi_password_entry.set_visible(False)
        self._contact_first_name_entry.set_visible(False)
        self._contact_last_name_entry.set_visible(False)
        self._contact_phone_entry.set_visible(False)
        self._contact_email_entry.set_visible(False)
        self._contact_birthday_row.set_visible(False)
        self._contact_url_entry.set_visible(False)
        self._contact_address_row.set_visible(False)

    def _on_generate_clicked(self, source: GObject.Object):

        match self._type_combo.get_selected():
            case 0:  # text
                img = qrcode.make(self._text_entry.get_text(
                ), image_factory=qrcode.image.svg.SvgPathFillImage)
            case 1:  # wifi
                # WIFI:S:<SSID>;T:<WEP|WPA|blank>;P:<PASSWORD>;;;
                match self._wifi_encryption_combo.get_selected():
                    case 0:  # WPA
                        encryption = f"T:WPA;P:{
                            self._wifi_password_entry.get_text()}"
                    case 1:  # WEP
                        encryption = f"T:WEP;P:{
                            self._wifi_password_entry.get_text()}"
                    case 2:  # None
                        encryption = ";"
                wifi = f"WIFI:S:{self._wifi_ssid_entry.get_text()};{
                    encryption};;"
                img = qrcode.make(
                    wifi, image_factory=qrcode.image.svg.SvgPathFillImage)
            case 2:  # contact
                # https://en.wikipedia.org/wiki/VCard

                # Check mandatory fields
                check = True
                if not self._contact_last_name_entry.get_text():
                    check = False
                    self._contact_last_name_entry.add_css_class("border-red")
                if not self._contact_first_name_entry.get_text():
                    check = False
                    self._contact_first_name_entry.add_css_class("border-red")
                if not check:
                    return

                contact = "BEGIN:VCARD\nVERSION:4.0\n"
                contact += f"FN:{self._contact_last_name_entry.get_text()
                                 },{self._contact_first_name_entry.get_text()}\n"

                # Optional fields
                if self._contact_phone_entry.get_text():
                    contact += f"TEL:{self._contact_phone_entry.get_text()}\n"
                if self._contact_email_entry.get_text():
                    contact += f"EMAIL:{self._contact_email_entry.get_text()}\n"
                if not self._contact_birthday_not_set_btn.get_active():
                    contact += f"BDAY:{
                        self._contact_birthday_calendar.get_date().format('%Y%m%d')}\n"
                if self._contact_url_entry.get_text():
                    contact += f"URL:{self._contact_url_entry.get_text()}\n"
                if self._contact_address_street_entry.get_text():
                    contact += f"ADR:;;{self._contact_address_street_entry.get_text()};"
                    contact += f"{self._contact_address_city_entry.get_text()};"
                    contact += f"{self._contact_address_state_entry.get_text()};"
                    contact += f"{self._contact_address_zip_entry.get_text()};"
                    contact += f"{self._contact_address_country_entry.get_text()}\n"

                contact += "END:VCARD"
                img = qrcode.make(
                    contact, image_factory=qrcode.image.svg.SvgPathFillImage)

        # show qrcode
        loader = GdkPixbuf.PixbufLoader()
        loader.write(img.to_string())
        loader.close()
        self.pixbuf = loader.get_pixbuf()
        self._qrcode_area.set_pixbuf(self.pixbuf)

    def _on_first_name_changed(self, user_data: GObject.GPointer):
        self._contact_first_name_entry.remove_css_class("border-red")

    def _on_last_name_changed(self, user_data: GObject.GPointer):
        self._contact_last_name_entry.remove_css_class("border-red")

    def _on_save_clicked(self, source: Gtk.Widget):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        self._file_dialog = Gtk.FileDialog(
            modal=True,
            title=_("Save file as"),
            accept_label=_("Save"),
            initial_name=self._qrcode_area.default_save_name
        )
        self._file_dialog.save(
            window, None, self._on_save_dialog_complete, None)
        return True    # Return true to block default handler

    def _on_save_dialog_complete(self, source: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        try:
            file = source.save_finish(result)
            self._save_file(file)
        except GLib.GError:
            pass

    def _save_file(self, destination: Gio.File):
        self.pixbuf.savev(destination.get_path(), "png", None, None)
        self._qrcode_area.set_file(destination)
        self._saved_toast.set_title(_("Saved Successfully"))
        self._toast.add_toast(self._saved_toast)
        self._save_path = destination.peek_path()

    def _on_view_clicked(self, source: Gtk.Widget):
        tmp = Gio.File.new_tmp("me.iepure.devtoolbox.XXXXXX.png")[0]
        self.pixbuf.savev(tmp.get_path(), "png", None, None)

        app = Gio.Application.get_default()
        window = app.get_active_window()
        Gtk.show_uri(window, tmp.get_uri(), Gdk.CURRENT_TIME)
        return True  # Return true to block default handler

    def _on_toast_btn_clicked(self, user_data: GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        Gtk.show_uri(window, "file://" + self._save_path, Gdk.CURRENT_TIME)
