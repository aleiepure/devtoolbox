# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk, GtkSource
from gettext import gettext as _

from devtoolbox.utils import Utils


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/text_area.ui')
class TextArea(Adw.Bin):
    __gtype_name__ = "TextArea"

    _name = Gtk.Template.Child()
    _separator = Gtk.Template.Child()
    _action_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _open_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _textview = Gtk.Template.Child()

    # Custom properties
    name = GObject.Property(type=str, default="")

    show_clear_btn = GObject.Property(type=bool, default=False)
    show_copy_btn = GObject.Property(type=bool, default=False)
    show_open_btn = GObject.Property(type=bool, default=False)
    show_paste_btn = GObject.Property(type=bool, default=False)
    show_action_btn = GObject.Property(type=bool, default=False)

    action_name = GObject.Property(type=str, default="")

    text_editable = GObject.Property(type=bool, default=True)
    text_show_line_numbers = GObject.Property(type=bool, default=False)
    text_highlight_current_line = GObject.Property(type=bool, default=False)
    text_syntax_highlighting = GObject.Property(type=bool, default=False)
    text_language_highlight = GObject.Property(type=str, default="")

    area_height = GObject.Property(type=int, default=200)

    use_default_text_extensions = GObject.Property(type=bool, default=False)
    use_custom_file_extensions = GObject.Property(type=bool, default=False)
    custom_file_extensions = GObject.Property(type=GObject.TYPE_STRV)

    # Custom signals
    __gsignals__ = {
        "action-clicked": (GObject.SIGNAL_RUN_LAST, None, ()),
        "text-changed": (GObject.SIGNAL_RUN_LAST, None, ()),
        "view-cleared": (GObject.SIGNAL_RUN_LAST, None, ()),
        "text-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "big-file": (GObject.SIGNAL_RUN_LAST, None, (GObject.TYPE_PYOBJECT,)),
        "error": (GObject.SIGNAL_RUN_LAST, None, (str,)),
    }

    def __init__(self):
        super().__init__()

       # Set syntax highlighting
        self._textview.get_buffer().set_language(
            GtkSource.LanguageManager.get_default().get_language(self.text_language_highlight))
        self._textview.get_buffer().set_style_scheme(
            GtkSource.StyleSchemeManager().get_default().get_scheme("Adwaita-dark"))

        # Bind properties
        self.bind_property("name", self._name, "label",
                           GObject.BindingFlags.SYNC_CREATE)

        self.bind_property("show-clear-btn", self._clear_btn,
                           "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-copy-btn", self._copy_btn,
                           "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-open-btn", self._open_btn,
                           "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-paste-btn", self._paste_btn,
                           "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-action-btn", self._action_btn,
                           "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-action-btn", self._separator,
                           "visible", GObject.BindingFlags.SYNC_CREATE)

        self.bind_property("action-name", self._action_btn,
                           "label", GObject.BindingFlags.SYNC_CREATE)

        self.bind_property("text-editable", self._textview,
                           "editable", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-syntax-highlighting", self._textview.get_buffer(),
                           "highlight-syntax", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-syntax-highlighting", self._textview.get_buffer(),
                           "highlight-matching-brackets", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-show-line-numbers", self._textview,
                           "show-line-numbers", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-highlight-current-line", self._textview,
                           "highlight-current-line", GObject.BindingFlags.SYNC_CREATE)

        self.bind_property("area-height", self._textview,
                           "height-request", GObject.BindingFlags.SYNC_CREATE)

        # Signals
        self._action_btn.connect("clicked", self._on_action_clicked)
        self._clear_btn.connect("clicked", self._on_clear_clicked)
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._open_btn.connect("clicked", self._on_open_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._textview.get_buffer().connect("changed", self._on_text_changed)

    def _on_action_clicked(self, data):
        self.emit("action-clicked")

    def _on_clear_clicked(self, data):
        self.clear()
        self.emit("view-cleared")

    def clear(self):
        self._textview.get_buffer().set_text("")
        self._textview.remove_css_class("border-red")

    def _on_copy_clicked(self, data):
        text_buffer = self._textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(),
                                    text_buffer.get_end_iter(), False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    def _on_paste_clicked(self, data):
        text_buffer = self._textview.get_buffer()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        text_buffer.paste_clipboard(clipboard, None, True)

    def _on_open_clicked(self, data):

        self._native = Gtk.FileChooserNative(
            title="Open File",
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel"
        )

        file_filter = Gtk.FileFilter()
        if self.use_default_text_extensions:
            file_filter.add_mime_type("text/*")
            file_filter.set_name(_("Text files"))
            self._native.add_filter(file_filter)
        if self.use_custom_file_extensions:
            for extension in self.custom_file_extensions:
                file_filter.add_suffix(extension)
            file_filter.set_name(_("Accepted files"))
            self._native.add_filter(file_filter)

        self._native.connect("response", self._on_open_response)
        self._native.show()

    def _on_open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self._open_file(dialog.get_file())

        self._native = None

    def _open_file(self, file):
        file_size = file.query_info("*", 0, None).get_size()

        if file_size > 1000000000:
            self.emit("big-file", file_size)

        file.load_contents_async(None, self._open_file_complete)

    def _open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)

        if not contents[0]:
            self.emit(
                "error", f"Unable to open {file.peek_path()}: {contents[1]}")
            return

        if Utils.is_text(contents[1]):
            text = contents[1].decode("utf-8")
        else:
            self.emit(
                "error", f"Unable to open {file.peek_path()}: content is not text")
            return

        text_buffer = self._textview.get_buffer()
        text_buffer.set_text(text)
        text_buffer.place_cursor(text_buffer.get_end_iter())
        self.emit("text-loaded")

    def _on_text_changed(self, data):
        self.emit("text-changed")

    def get_text(self):
        text_buffer = self._textview.get_buffer()
        return text_buffer.get_text(text_buffer.get_start_iter(),
                                    text_buffer.get_end_iter(), False)

    def set_text(self, text):
        text_buffer = self._textview.get_buffer()
        text_buffer.set_text(text, -1)

    def get_buffer(self):
        return self._textview.get_buffer()

    def set_text_language_highlight(self, language):
        self._textview.get_buffer().set_language(
            GtkSource.LanguageManager.get_default().get_language(language))

    def add_css_class(self, css_class):
        self._textview.add_css_class(css_class)

    def remove_css_class(self, css_class):
        self._textview.remove_css_class(css_class)

    def enable_copy_btn(self, enabled):
        self._copy_btn.set_sensitive(enabled)
