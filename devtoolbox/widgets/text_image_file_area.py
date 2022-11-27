# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk, GLib, GtkSource
from gettext import gettext as _
import humanize

from devtoolbox.utils import Utils


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/text_image_file_area.ui')
class TextImageFileArea(Adw.Bin):

    __gtype_name__ = "TextImageFileArea"

    _name = Gtk.Template.Child()
    _separator = Gtk.Template.Child()
    _action_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _open_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _textview = Gtk.Template.Child()
    _imageview = Gtk.Template.Child()
    _file_path_label = Gtk.Template.Child()
    _file_size_label = Gtk.Template.Child()
    _stack = Gtk.Template.Child()
    _loading = Gtk.Template.Child()
    _loading_label = Gtk.Template.Child()

    _image = []
    _file_path = ""
    input_type = "text"

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
    use_default_image_extensions = GObject.Property(type=bool, default=False)
    use_all_files_extensions = GObject.Property(type=bool, default=False)
    use_custom_file_extensions = GObject.Property(type=bool, default=False)
    custom_file_extensions = GObject.Property(type=GObject.TYPE_STRV)

    loading_label = GObject.Property(type=str, default="")

    # Custom signals
    __gsignals__ = {
        "action-clicked": (GObject.SIGNAL_RUN_LAST, None, ()),
        "text-changed": (GObject.SIGNAL_RUN_LAST, None, ()),
        "view-cleared": (GObject.SIGNAL_RUN_LAST, None, ()),
        "text-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "image-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "file-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "big-file": (GObject.SIGNAL_RUN_LAST, None, (GObject.TYPE_PYOBJECT,)),
        "error": (GObject.SIGNAL_RUN_LAST, None, (str,))
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

        self.bind_property("loading-label", self._loading_label,
                           "label", GObject.BindingFlags.SYNC_CREATE)

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
        self.input_type = "text"
        self._textview.get_buffer().set_text("")
        self._image = []
        self._file_path = ""
        self._stack.set_visible_child_name("text")
        self._textview.remove_css_class("border-red")

    def _on_copy_clicked(self, data):
        text_buffer = self._textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(),
                                    text_buffer.get_end_iter(), False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)
        self._image = []
        self._file_path = ""
        self._stack.set_visible_child_name("text")

    def _on_paste_clicked(self, data):
        text_buffer = self._textview.get_buffer()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        text_buffer.paste_clipboard(clipboard, None, True)
        self._image = []
        self._stack.set_visible_child_name("text")

    def _on_open_clicked(self, data):

        self._stack.set_visible_child_name("loading")

        self._native = Gtk.FileChooserNative(
            title="Open File",
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel"
        )

        if self.use_all_files_extensions:
            all_files_filter = Gtk.FileFilter()
            all_files_filter.add_pattern("*")
            all_files_filter.set_name(_("All files"))
            self._native.add_filter(all_files_filter)
        if self.use_default_text_extensions and self.use_default_image_extensions:
            text_image_file_filter = Gtk.FileFilter()
            text_image_file_filter.add_mime_type("text/*")
            text_image_file_filter.add_pixbuf_formats()
            text_image_file_filter.set_name(_("Text and image files"))
            self._native.add_filter(text_image_file_filter)
        if self.use_default_text_extensions:
            text_file_filter = Gtk.FileFilter()
            text_file_filter.add_mime_type("text/*")
            text_file_filter.set_name(_("Text files"))
            self._native.add_filter(text_file_filter)
        if self.use_default_image_extensions:
            image_file_filter = Gtk.FileFilter()
            image_file_filter.add_pixbuf_formats()
            image_file_filter.set_name(_("Image files"))
            self._native.add_filter(image_file_filter)
        if self.use_custom_file_extensions:
            custom_file_filter = Gtk.FileFilter()
            for extension in self.custom_file_extensions:
                custom_file_filter.add_suffix(extension.lstrip().rstrip())
            custom_file_filter.set_name(_("Accepted files"))
            self._native.add_filter(custom_file_filter)

        self._native.connect("response", self._on_open_response)
        self._native.show()

    def _on_open_response(self, dialog, response):

        if response == Gtk.ResponseType.ACCEPT:
            self._open_file(dialog.get_file())
        else:
            self._stack.set_visible_child_name(self.input_type)

        self._native = None

    def _open_file(self, file):
        file_path = file.peek_path()
        file_size = file.query_info("*", 0, None).get_size()

        if file_size > 1000000000:
            self._stack.set_visible_child_name("file")
            self._file_path_label.set_label(file_path)
            self._file_size_label.set_label(humanize.naturalsize(file_size))
            self.emit("big-file", file_size)
            self.emit("file-loaded")
        else:
            file.load_contents_async(None, self._open_file_complete)

    def _open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)

        if not contents[0]:
            self.emit(
                "error", f"Unable to open {file.peek_path()}: {contents[1]}")
            return

        if Utils.is_text(contents[1]):
            text = contents[1].decode("utf-8")
            self.input_type = "text"
        elif Utils.is_image(contents[1]):
            self._image = contents[1]
            file_path = file.peek_path()
            texture = Gdk.Texture.new_from_bytes(GLib.Bytes(contents[1]))
            self.input_type = "image"
        else:
            file_path = file.peek_path()
            file_size = file.query_info("*", 0, None).get_size()
            self.input_type = "file"

        if self.input_type == "text":
            self._stack.set_visible_child_name("text")
            text_buffer = self._textview.get_buffer()
            text_buffer.set_text(text)
            text_buffer.place_cursor(text_buffer.get_end_iter())
            self.emit("text-loaded")
        elif self.input_type == "image":
            self._stack.set_visible_child_name("image")
            self._file_path_label.set_label(file_path)
            self._imageview.set_paintable(texture)
            self.emit("image-loaded")
        else:
            self._stack.set_visible_child_name("file")
            self._file_path_label.set_label(file_path)
            self._file_size_label.set_label(humanize.naturalsize(file_size))
            self.emit("file-loaded")

    def _on_text_changed(self, data):
        self.emit("text-changed")

    def get_text(self):
        text_buffer = self._textview.get_buffer()
        return text_buffer.get_text(text_buffer.get_start_iter(),
                                    text_buffer.get_end_iter(), False)

    def get_buffer(self):
        return self._textview.get_buffer()

    def add_css_class(self, css_class):
        self._textview.add_css_class(css_class)
        self._imageview.add_css_class(css_class)

    def remove_css_class(self, css_class):
        self._textview.remove_css_class(css_class)
        self._imageview.remove_css_class(css_class)

    def get_visible_view(self):
        return self._stack.get_visible_child_name()

    def set_visible_view(self, child):
        self._stack.set_visible_child_name(child)

    def get_image(self):
        return self._image

    def get_file_path(self):
        return self._file_path_label.get_label()

    def set_image(self, texture):
        self._stack.set_visible_child_name("image")
        self._imageview.set_paintable(texture)

    def enable_copy_btn(self, enabled):
        self._copy_btn.set_sensitive(enabled)

    def set_text_language_highlight(self, language):
        self._textview.get_buffer().set_language(
            GtkSource.LanguageManager.get_default().get_language(language))

    def set_loading_visible(self, enabled):
        self._loading.set_visible(enabled)
