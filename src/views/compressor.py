# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gdk, GLib, Gio, GObject
from gettext import gettext as _

from ..utils import Utils
from ..services.compressor import CompressorService
from ..compressors.compressor import Compressor


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/compressor.ui")
class CompressorView(Adw.Bin):
    __gtype_name__ = "CompressorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _direction_selector = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    # Toast messages
    _file_saved_toast = Adw.Toast(
        priority=Adw.ToastPriority.HIGH, button_label=_("Open image"))
    _error_toast = Adw.Toast(priority=Adw.ToastPriority.HIGH)
    _cannot_convert_toast = Adw.Toast(title=_(
        "Cannot decompress from an image or a file"), priority=Adw.ToastPriority.HIGH)

    def __init__(self, compressor: Compressor):
        super().__init__()

        # Initialize service with specific compressor
        self._service = CompressorService(compressor)

        # Set title
        self._title.set_property("title", compressor.get_title())
        self._title.set_property("description", compressor.get_description())
        self._title.set_property("tool-name", compressor.get_utility_name())

        # Signals
        self._file_saved_toast.connect(
            "button-clicked", self._on_toast_button_clicked_signal)

    @Gtk.Template.Callback()
    def _on_direction_changed_signal(self,
                                     pspec: GObject.GParamSpec,
                                     user_data: GObject.GPointer = None) -> None:
        self._convert()

    @Gtk.Template.Callback()
    def _on_input_changed_signal(self, source_widget: GObject.Object):
        self._convert()

    def _on_toast_button_clicked_signal(self, user_data: GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        Gtk.show_uri(window, "file://" + self._save_path, Gdk.CURRENT_TIME)

    @Gtk.Template.Callback()
    def _on_file_saved_signal(self, source_object: GObject.Object, file_path: str):
        self._file_saved_toast.set_title(_("Saved Successfully"))
        self._toast.add_toast(self._file_saved_toast)
        self._save_path = file_path

    @Gtk.Template.Callback()
    def _on_view_cleared_signal(self, source_widget: GObject.Object):
        self._output_area.set_property("show-copy-btn", True)
        self._output_area.set_property("show-save-btn", False)
        self._output_area.set_property("show-spinner", False)
        self._output_area.clear()

    @Gtk.Template.Callback()
    def _on_error_signal(self, source_widget: GObject.Object, error: str):
        self._error_toast.set_title(_("Error: {error}").format(error=error))
        self._toast.add_toast(self._error_toast)

    def _convert(self):

        # Stop previous tasks
        if hasattr(self, '_current_cancellable') and self._current_cancellable:
            self._current_cancellable.cancel()

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
        if self._direction_selector.get_active() == 0:  # Compress
            if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
                self._service.compress_text_async(
                    self, self._on_async_done, None)
                self._current_cancellable = self._service.get_cancellable()
            elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
                self._output_area.clear()
                self._output_area.set_spinner_spin(False)
            else:
                self._service.compress_bytes_async(
                    self, self._on_async_done, None)
                self._current_cancellable = self._service.get_cancellable()
        else:  # Decompress
            if self._input_area.get_visible_view() == "text-area" and len(text) > 0 and Utils.is_base64(text):
                self._service.decompress_async(self, self._on_async_done, None)
                self._current_cancellable = self._service.get_cancellable()
            elif self._input_area.get_visible_view() == "text-area" and len(text) > 0 and (not Utils.is_base64(text)):
                self._input_area.add_css_class("border-red")
                self._output_area.clear()
                self._output_area.set_spinner_spin(False)
            elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
                self._output_area.clear()
                self._output_area.set_spinner_spin(False)
            else:
                self._output_area.clear()
                self._input_area.add_css_class("border-red")
                self._toast.add_toast(self._cannot_convert_toast)
                self._output_area.set_spinner_spin(False)

    def _on_async_done(self, source_widget: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        self._output_area.set_spinner_spin(False)

        try:
            outcome = self._service.async_finish(result, self)
            if not outcome:  # Empty result
                return
        except GLib.Error as e:
            if e.code == Gio.IOErrorEnum.CANCELLED:
                return  # Silently ignore cancellation
            self._error_toast.set_title(
                _("Error: {error}").format(error=str(e)))
            self._toast.add_toast(self._error_toast)
            return
        except Exception as e:
            self._error_toast.set_title(
                _("Error: {error}").format(error=str(e)))
            self._toast.add_toast(self._error_toast)
            return

        if isinstance(outcome, GLib.Bytes):
            data = outcome.get_data()
            if Utils.is_text(data):
                self._output_area.set_text(
                    data.decode("utf-8", errors="replace"))
                self._output_area.set_visible_view("text-area")
                self._output_area.set_property("show-copy-btn", True)
                self._output_area.set_property("show-save-btn", False)
            elif Utils.is_image(data):
                self._output_area.clear()
                self._output_area.set_image(outcome)
                self._output_area.set_visible_view("image-area")
                self._output_area.set_property("show-copy-btn", False)
                self._output_area.set_property("show-save-btn", True)
            else:
                self._output_area.clear()
                self._output_area.set_file(outcome, _(
                    "Please save this file to view its contents"))
                self._output_area.set_visible_view("file-area")
                self._output_area.set_property("show-copy-btn", False)
                self._output_area.set_property("show-save-btn", True)

        elif isinstance(outcome, str) and len(outcome) > 0:
            self._output_area.set_text(outcome)
            self._output_area.set_visible_view("text-area")
            self._output_area.set_property("show-copy-btn", True)
            self._output_area.set_property("show-save-btn", False)
