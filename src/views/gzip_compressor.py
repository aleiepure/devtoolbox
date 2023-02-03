# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gdk, GLib
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

    def __init__(self):
        super().__init__()

        # Signals
        self._direction_selector.connect("toggled", self._convert)
        self._input_area.connect("text-changed", self._convert)
        self._input_area.connect("image-loaded", self._convert)
        self._input_area.connect("file-loaded", self._convert)
        self._input_area.connect("error", self._on_error)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._output_area.connect("error", self._on_error)
        self._output_area.connect("saved", self._on_saved)

    def _on_saved(self, data, file_name):
        self._output_area.set_file_path(file_name)
        self._toast.add_toast(Adw.Toast(title=f'{_("Successfully saved as")} {file_name}', priority=Adw.ToastPriority.HIGH))

    def _on_view_cleared(self, data):
        self._output_area.set_save_btn_visible(False)
        self._output_area.set_copy_btn_visible(True)
        self._output_area.clear()

    def _on_error(self, data, error):
        error_str = _("Error")
        self._toast.add_toast(Adw.Toast(title=f"{error_str}: {error}", priority=Adw.ToastPriority.HIGH))

    def _convert(self, data):

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
            file_contents = self._input_area.get_file_contents()
            self._service.set_input(file_contents[1])

        # Call task
        if self._direction_selector.get_left_active():
            if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
                self._service.compress_text_async(self, self._on_async_done)
            elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
                self._output_area.clear()
            else:
                self._service.compress_bytes_async(self, self._on_async_done)
        else:
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
                self._toast.add_toast(Adw.Toast(title=_("Cannot decompress from image or file"), priority=Adw.ToastPriority.HIGH))

    def _on_async_done(self, source_object, result, data):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.async_finish(result, self)

        if len(outcome)>0 and Utils.is_text(outcome):
            if isinstance(outcome, str):
                self._output_area.set_text(outcome)
            else:
                self._output_area.set_text(outcome.decode("utf-8"))
            self._output_area.set_visible_view("text-area")
            self._output_area.set_save_btn_visible(False)
            self._output_area.set_copy_btn_visible(True)
        elif len(outcome)>0 and Utils.is_image(outcome):
            self._output_area.clear()
            self._output_area.set_image(GLib.Bytes(outcome))
            self._output_area.set_visible_view("image-area")
            self._output_area.set_save_btn_visible(True)
            self._output_area.set_copy_btn_visible(False)
        elif len(outcome)>0:
            self._output_area.clear()
            self._output_area.set_file(GLib.Bytes(outcome), _("Please save this file to view its contents"))
            self._output_area.set_visible_view("file-area")
            self._output_area.set_save_btn_visible(True)
            self._output_area.set_copy_btn_visible(False)
