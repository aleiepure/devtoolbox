# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gdk, GLib, Gio, GObject
from gettext import gettext as _

from ..utils import Utils
from ..services.gzip_compressor import GzipCompressorService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/gzip_compressor.ui")
class GzipCompressorView(Adw.Bin):
    __gtype_name__ = "GzipCompressorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _direction_selector = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    # Service
    _service = GzipCompressorService()

    # Toast messages
    _file_saved_toast = Adw.Toast(priority=Adw.ToastPriority.HIGH, button_label=_("Open folder"))
    _error_toast = Adw.Toast(priority=Adw.ToastPriority.HIGH)
    _cannot_convert = Adw.Toast(title=_("Cannot decompress from an image or a file"), priority=Adw.ToastPriority.HIGH)

    def __init__(self):
        super().__init__()

        # Signals
        self._direction_selector.connect("toggled", self._on_input_changed)
        self._input_area.connect("text-changed", self._on_input_changed)
        self._input_area.connect("image-loaded", self._on_input_changed)
        self._input_area.connect("file-loaded", self._on_input_changed)
        self._input_area.connect("error", self._on_error)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._output_area.connect("error", self._on_error)
        self._output_area.connect("saved", self._on_file_saved)
        self._file_saved_toast.connect("button-clicked", self._on_toast_button_clicked)

    def _on_input_changed(self, source_widget:GObject.Object):
        self._convert()

    def _on_toast_button_clicked(self, user_data:GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        full_msg = self._file_saved_toast.get_title()
        full_path = full_msg[full_msg.index("/"):len(full_msg)]
        folder_path = full_path[:full_path.rindex("/")]
        Gtk.show_uri(window, "file://" + folder_path, Gdk.CURRENT_TIME)

    def _on_file_saved(self, source_objcet:GObject.Object, file_path:str):
        self._output_area.set_file_path(file_path)
        self._file_saved_toast.set_title(_("Successfully saved as {save_path}").format(save_path=file_path))
        self._toast.add_toast(self._file_saved_toast)

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._output_area.set_property("show-copy-btn" , True)
        self._output_area.set_property("show-save-btn" , False)
        self._output_area.clear()

    def _on_error(self, source_widget:GObject.Object, error:str):
        self._error_toast.set_title(_("Error: {error}").format(error=error))
        self._toast.add_toast(self._error_toast)

    def _convert(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        self._output_area.set_spinner_spin(True)
        text = self._input_area.get_text()
        if self._input_area.get_visible_view() == "text-area":
            self._service.set_input(text)
        else:
            self._service.set_input(self._input_area.get_opened_file_path())

        # Call task
        if self._direction_selector.get_left_btn_active(): # Compress
            if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
                self._service.compress_text_async(self, self._on_async_done)
            elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
                self._output_area.clear()
            else:
                self._service.compress_bytes_async(self, self._on_async_done)
        else: # Decompress
            if self._input_area.get_visible_view() == "text-area" and len(text) > 0 and Utils.is_base64(text):
                self._service.decompress_async(self, self._on_async_done)
            elif self._input_area.get_visible_view() == "text-area" and len(text) > 0 and (not Utils.is_base64(text)):
                self._input_area.add_css_class("border-red")
                self._output_area.clear()
            elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
                self._output_area.clear()
            else:
                self._output_area.clear()
                self._input_area.add_css_class("border-red")
                self._toast.add_toast(self._cannot_convert_toast)

    def _on_async_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.async_finish(result, self)

        if len(outcome)>0 and Utils.is_text(outcome):
            if isinstance(outcome, str):
                self._output_area.set_text(outcome)
            else:
                self._output_area.set_text(outcome.decode("utf-8"))
            self._output_area.set_visible_view("text-area")
            self._output_area.set_property("show-copy-btn" , True)
            self._output_area.set_property("show-save-btn" , False)
        elif len(outcome)>0 and Utils.is_image(outcome):
            self._output_area.clear()
            self._output_area.set_image(GLib.Bytes(outcome))
            self._output_area.set_visible_view("image-area")
            self._output_area.set_property("show-copy-btn" , False)
            self._output_area.set_property("show-save-btn" , True)
        elif len(outcome)>0:
            self._output_area.clear()
            self._output_area.set_file(GLib.Bytes(outcome), _("Please save this file to view its contents"))
            self._output_area.set_visible_view("file-area")
            self._output_area.set_property("show-copy-btn" , False)
            self._output_area.set_property("show-save-btn" , True)
