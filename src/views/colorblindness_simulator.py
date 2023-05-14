# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, Gdk
from gettext import gettext as _

from ..services.colorblindness_simulator import ColorblindnessSimulatorService


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/colorblindness_simulator.ui')
class ColorblindnessSimulatorView(Adw.Bin):
    __gtype_name__ = "ColorblindnessSimulatorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _severity_scale = Gtk.Template.Child()
    _original_imagearea = Gtk.Template.Child()
    _protanopia_imagearea = Gtk.Template.Child()
    _deuteranopia_imagearea = Gtk.Template.Child()
    _tritanopia_imagearea = Gtk.Template.Child()

    _service = ColorblindnessSimulatorService()

    _saved_toast = Adw.Toast(priority=Adw.ToastPriority.HIGH, button_label=_("Open folder"))

    def __init__(self):
        super().__init__()

        # Marks
        #self._severity_scale.add_mark(0.8, Gtk.PositionType.BOTTOM, None)
        self._severity_scale.remove_css_class("marks-after")

        # Signals
        self._original_imagearea.connect("view-cleared", self._on_view_cleared)
        self._original_imagearea.connect("image-loaded", self._on_image_loaded)
        self._severity_scale.connect("value-changed", self._on_severity_changed_by_keyboard)
        self._severity_scale.connect("notify::css-classes", self._on_severity_changed_by_mouse)

        self._protanopia_imagearea.connect("saved", self._on_saved)
        self._deuteranopia_imagearea.connect("saved", self._on_saved)
        self._tritanopia_imagearea.connect("saved", self._on_saved)
        self._saved_toast.connect("button-clicked", self._on_toast_btn_clicked)

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._protanopia_imagearea.clear()
        self._deuteranopia_imagearea.clear()
        self._tritanopia_imagearea.clear()
        self._service.get_cancellable().cancel()

    def _on_severity_changed_by_keyboard(self, user_data:GObject.GPointer):
        if self._severity_scale.has_css_class("dragging"):
            return
        self._service.get_cancellable().cancel()
        self._simulate()

    def _on_severity_changed_by_mouse(self, source_widget:GObject.Object, user_data:GObject.GPointer):
        if not self._severity_scale.has_css_class("dragging"):
            self._service.get_cancellable().cancel()
            self._simulate()

    def _on_image_loaded(self, source_widget:GObject.Object):
        self._simulate()

    def _on_saved(self, source_widget:GObject.Object, path:str):
        self._saved_toast.set_title(_("Successfully saved as {save_path}").format(save_path=path))
        self._toast.add_toast(self._saved_toast)

    def _on_toast_btn_clicked(self, user_data:GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        full_msg = self._saved_toast.get_title()
        full_path = full_msg[full_msg.index("/"):len(full_msg)]
        folder_path = full_path[:full_path.rindex("/")]
        Gtk.show_uri(window, "file://" + folder_path, Gdk.CURRENT_TIME)

    def _simulate(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._protanopia_imagearea.clear()
        self._deuteranopia_imagearea.clear()
        self._tritanopia_imagearea.clear()

        # Setup task
        original_file = self._original_imagearea.get_file()
        severity = self._severity_scale.get_value()
        self._service.set_original_file(original_file)
        self._service.set_severity(severity)

        # Call task
        if original_file:
            self._protanopia_imagearea.set_loading_lbl(_("Loading simulation..."))
            self._protanopia_imagearea.set_visible_view("loading")
            self._deuteranopia_imagearea.set_loading_lbl(_("Loading simulation..."))
            self._deuteranopia_imagearea.set_visible_view("loading")
            self._tritanopia_imagearea.set_loading_lbl(_("Loading simulation..."))
            self._tritanopia_imagearea.set_visible_view("loading")
            self._service.simulate_async(self, self._on_async_done)

    def _on_async_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        protanopia_file, deutranopia_file, tritanopia_file = self._service.async_finish(result, self)
        self._protanopia_imagearea.set_file(protanopia_file)
        self._protanopia_imagearea.set_visible_view("image")
        self._deuteranopia_imagearea.set_file(deutranopia_file)
        self._deuteranopia_imagearea.set_visible_view("image")
        self._tritanopia_imagearea.set_file(tritanopia_file)
        self._tritanopia_imagearea.set_visible_view("image")
