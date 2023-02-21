# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GtkSource, Gdk, GLib
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
    _deutranopia_imagearea = Gtk.Template.Child()
    _tritanopia_imagearea = Gtk.Template.Child()

    _service = ColorblindnessSimulatorService()

    def __init__(self):
        super().__init__()

        self._severity_scale.remove_css_class("marks-after")

        # Signals
        self._original_imagearea.connect("view-cleared", self._on_view_cleared)
        self._original_imagearea.connect("image-loaded", self._on_image_loaded)
        self._severity_scale.connect("notify::css-classes", self._on_severity_changed)

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._protanopia_imagearea.clear()
        self._deutranopia_imagearea.clear()
        self._tritanopia_imagearea.clear()
        self._service.get_cancellable().cancel()

    def _on_severity_changed(self, source_widget:GObject.Object, user_data:GObject.GPointer):
        if not self._severity_scale.has_css_class("dragging"):
            self._service.get_cancellable().cancel()
            self._simulate()

    def _on_image_loaded(self, source_widget:GObject.Object):
        self._simulate()

    def _simulate(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._protanopia_imagearea.clear()
        self._deutranopia_imagearea.clear()
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
            self._deutranopia_imagearea.set_loading_lbl(_("Loading simulation..."))
            self._deutranopia_imagearea.set_visible_view("loading")
            self._tritanopia_imagearea.set_loading_lbl(_("Loading simulation..."))
            self._tritanopia_imagearea.set_visible_view("loading")
            self._service.simulate_async(self, self._on_async_done)

    def _on_async_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        protanopia_file, deutranopia_file, tritanopia_file = self._service.async_finish(result, self)
        self._protanopia_imagearea.set_file(protanopia_file)
        self._protanopia_imagearea.set_visible_view("image")
        self._deutranopia_imagearea.set_file(deutranopia_file)
        self._deutranopia_imagearea.set_visible_view("image")
        self._tritanopia_imagearea.set_file(tritanopia_file)
        self._tritanopia_imagearea.set_visible_view("image")
