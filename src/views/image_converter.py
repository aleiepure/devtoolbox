# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gio, GObject, Gdk, GLib
from gettext import gettext as _

from ..services.image_converter import ImageConverterService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/image_converter.ui")
class ImageConverterView(Adw.Bin):
    __gtype_name__ = "ImageConverterView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _format_combo = Gtk.Template.Child()
    _imagearea = Gtk.Template.Child()

    _service = ImageConverterService()

    _saved_toast = Adw.Toast(
        priority=Adw.ToastPriority.HIGH, button_label=_("Open Image"))

    def __init__(self):
        super().__init__()

        # Signals
        self._imagearea.connect("action-clicked", self._on_action_clicked)
        self._saved_toast.connect("button-clicked", self._on_toast_btn_clicked)

    def _on_action_clicked(self, source_widget: GObject.Object):
        if self._imagearea.get_file():
            self._imagearea.set_action_btn_sensitive(False)
            self._service.get_cancellable().cancel()
            self._get_destination_file_and_setup_task()

    def _on_convertion_done(self, source_widget: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        converted_file_path = self._service.async_finish(result, self)
        self._saved_toast.set_title(_("Saved Successfully"))
        self._toast.add_toast(self._saved_toast)
        self._save_path = converted_file_path
        self._imagearea.set_action_btn_sensitive(True)

    def _get_destination_file_and_setup_task(self):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        self._file_dialog = Gtk.FileDialog(
            modal=True,
            title=_("Save file as"),
            accept_label=_("Save"),
        )
        match self._format_combo.get_selected():
            case 0:  # BMP
                extension = ".bmp"
            case 1:  # GIF
                extension = ".gif"
            case 2:  # ICNS
                extension = ".icns"
            case 3:  # JPEG
                extension = ".jpeg"
            case 4:  # PNG
                extension = ".png"
            case 5:  # TIFF
                extension = ".tiff"
            case 6:  # WEBP
                extension = ".webp"

        self._file_dialog.set_initial_name(
            self._imagearea.default_save_name + extension)
        self._file_dialog.save(
            window, None, self._on_save_dialog_complete, None)

    def _on_save_dialog_complete(self, source: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        try:
            selected_file = source.save_finish(result)
            image_file = self._imagearea.get_file()
            destination_format = self._format_combo.get_selected()
            self._service.set_file(image_file)
            self._service.set_destination_format(destination_format)
            self._service.set_destination_file(selected_file)

            # Call task
            if image_file:
                self._service.convert_image_async(
                    self, self._on_convertion_done)
        except GLib.GError:
            self._imagearea.set_action_btn_sensitive(True)

    def _on_toast_btn_clicked(self, user_data: GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        Gtk.show_uri(window, "file://" + self._save_path, Gdk.CURRENT_TIME)
