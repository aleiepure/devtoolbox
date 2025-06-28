# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gio, GObject

from ..services.markdown_preview import MarkdownPreviewService


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/markdown_preview.ui')
class MarkdownPreviewView(Adw.Bin):
    __gtype_name__ = "MarkdownPreviewView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _textarea = Gtk.Template.Child()
    _webarea = Gtk.Template.Child()

    _service = MarkdownPreviewService()

    def __init__(self):
        super().__init__()

        self._textarea.set_text_language_highlight("markdown")

        # Signals
        self._textarea.connect("text-changed", self._on_input_changed)
        self._textarea.connect("view-cleared", self._on_view_cleared)
        Adw.StyleManager.get_default().connect("notify::dark", self._on_style_changed)

        self._load_markdown()

    def _on_view_cleared(self, source_widget: GObject.Object):
        self._service.get_cancellable().cancel()

    def _on_input_changed(self, source_widget: GObject.Object):
        self._load_markdown()
        
    def _on_style_changed(self, pspec: GObject.ParamSpec, user_data: GObject.GPointer):
        self._load_markdown()

    def _load_markdown(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()

        # Setup task
        self._service.set_markdown(self._textarea.get_text())

        # Call task
        self._service.build_html_from_markdown_async(self, self._on_build_done)

    def _on_build_done(self, source_widget: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        html_path = self._service.async_finish(result, self)
        self._webarea.load_uri("file://" + html_path)
