# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GtkSource, Gdk, GLib
from gettext import gettext as _
from typing import List
import humanize

from devtoolbox.utils import Utils


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/text_file_area.ui')
class TextFileArea(Adw.Bin):
    __gtype_name__ = "TextFileArea"

    # Template elements
    _name_lbl = Gtk.Template.Child()
    _spinner = Gtk.Template.Child()
    _spinner_separator = Gtk.Template.Child()
    _action_btn = Gtk.Template.Child()
    _action_btn_separator = Gtk.Template.Child()
    _view_btn = Gtk.Template.Child()
    _open_btn = Gtk.Template.Child()
    _save_btn = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()
    _stack = Gtk.Template.Child()
    _textview = Gtk.Template.Child()
    _imageview = Gtk.Template.Child()
    _fileview = Gtk.Template.Child()
    _loading_lbl = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    # Properties
    name = GObject.Property(type=str, default="")
    show_spinner = GObject.Property(type=bool, default=False)
    show_view_btn = GObject.Property(type=bool, default=False)
    show_clear_btn = GObject.Property(type=bool, default=False)
    show_save_btn = GObject.Property(type=bool, default=False)
    show_copy_btn = GObject.Property(type=bool, default=False)
    show_open_btn = GObject.Property(type=bool, default=False)
    show_paste_btn = GObject.Property(type=bool, default=False)
    show_action_btn = GObject.Property(type=bool, default=False)
    action_btn_name = GObject.Property(type=str, default="")
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
    loading_label = GObject.Property(type=str, default="Opening file...")
    allow_drag_and_drop = GObject.Property(type=bool, default=True)

    # Custom signals
    __gsignals__ = {
        "action-clicked": (GObject.SIGNAL_RUN_LAST, None, ()),
        "text-changed": (GObject.SIGNAL_RUN_LAST, None, ()),
        "view-cleared": (GObject.SIGNAL_RUN_LAST, None, ()),
        "text-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "image-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "file-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "big-file": (GObject.SIGNAL_RUN_LAST, None, ()),
        "error": (GObject.SIGNAL_RUN_LAST, None, (str,)),
        "saved": (GObject.SIGNAL_RUN_LAST, None, (str,)),
    }

    def __init__(self):
        super().__init__()

        # Set syntax highlighting
        language = GtkSource.LanguageManager.get_default().get_language(self.text_language_highlight)
        style_from_settings = self._settings.get_string("style-scheme")
        style_scheme = GtkSource.StyleSchemeManager().get_default().get_scheme(style_from_settings)
        self._textview.get_buffer().set_language(language)
        self._textview.get_buffer().set_style_scheme(style_scheme)

        # Drag and drop
        content = Gdk.ContentFormats.new_for_gtype(Gdk.FileList)
        target = Gtk.DropTarget(formats=content, actions=Gdk.DragAction.COPY)
        target.connect('drop', self._on_dnd_drop)
        self._textview.add_controller(target)

        # Property binding
        self.bind_property("name", self._name_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner_separator, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-view-btn", self._view_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-clear-btn", self._clear_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-copy-btn", self._copy_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-open-btn", self._open_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-save-btn", self._save_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-paste-btn", self._paste_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-action-btn", self._action_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-action-btn", self._action_btn_separator, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("action-btn-name", self._action_btn, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-editable", self._textview, "editable", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-syntax-highlighting", self._textview.get_buffer(), "highlight-syntax", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-syntax-highlighting", self._textview.get_buffer(), "highlight-matching-brackets", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-show-line-numbers", self._textview, "show-line-numbers", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("text-highlight-current-line", self._textview, "highlight-current-line", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("area-height", self._textview, "height-request", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("loading-label", self._loading_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self._spinner.bind_property("spinning", self._spinner, "visible", GObject.BindingFlags.BIDIRECTIONAL)
        self._spinner.bind_property("visible", self._spinner_separator, "visible", GObject.BindingFlags.BIDIRECTIONAL)
        self._action_btn.bind_property("visible", self._action_btn_separator, "visible", GObject.BindingFlags.BIDIRECTIONAL)

        # Signal connection
        self._action_btn.connect("clicked", self._on_action_clicked)
        self._view_btn.connect("clicked", self._on_view_clicked)
        self._clear_btn.connect("clicked", self._on_clear_clicked)
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._open_btn.connect("clicked", self._on_open_clicked)
        self._save_btn.connect("clicked", self._on_save_clicked)
        self._textview.get_buffer().connect("changed", self._on_text_changed)

    def _on_dnd_drop(self, drop_target:Gtk.DropTarget, value: Gdk.FileList, x:float, y:float, user_data:GObject.Object=None):
        self._spinner.set_visible(True)
        files: List[Gio.File] = value.get_files()
        if len(files) != 1:
            self.emit("error", "Cannot open more than one file")
            return
        self._open_file(files[0])
        self._spinner.set_visible(False)

    def _on_view_clicked(self, user_data:GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        Gtk.show_uri(window, "file://" + self._fileview.get_file_path(), Gdk.CURRENT_TIME)

    def _on_action_clicked(self, user_data:GObject.GPointer):
        self.emit("action-clicked")

    def _on_clear_clicked(self, user_data:GObject.GPointer):
        self._clear()
        self._open_btn.set_sensitive(True)
        self.emit("view-cleared")

    def _on_copy_clicked(self, user_data:GObject.GPointer):
        text_buffer = self._textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)
        self.set_visible_view("text-area")

    def _on_paste_clicked(self, user_data:GObject.GPointer):
        text_buffer = self._textview.get_buffer()
        clipboard   = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        text_buffer.paste_clipboard(clipboard, None, True)
        self.set_visible_view("text-area")

    def _on_open_clicked(self, user_data:GObject.GPointer):

        # Start loading animation and disable open button
        self._open_btn.set_sensitive(False)
        self.set_visible_view("loading") # change view and save previous
        self.loading_lbl = _("Opening file...")

        # Create a file chooser
        app = Gio.Application.get_default()
        window = app.get_active_window()
        self._native = Gtk.FileChooserNative(
            transient_for=window,
            title=_("Open File"),
            action=Gtk.FileChooserAction.OPEN,
            accept_label=_("Open"),
            cancel_label=_("Cancel")
        )

        # File filters
        if self.use_all_files_extensions:
            all_files_filter = Gtk.FileFilter()
            all_files_filter.add_pattern("*")
            all_files_filter.set_name(_("All files"))
            self._native.add_filter(all_files_filter)

        if self.use_default_text_extensions and self.use_default_image_extensions:
            text_image_filter = Gtk.FileFilter()
            text_image_filter.add_mime_type("text/*")
            text_image_filter.add_pixbuf_formats()
            text_image_filter.set_name(_("Text files and images"))
            self._native.add_filter(text_image_filter)

        if self.use_default_text_extensions:
            text_file_filter = Gtk.FileFilter()
            text_file_filter.add_mime_type("text/*")
            text_file_filter.set_name(_("Text files"))
            self._native.add_filter(text_file_filter)

        if self.use_default_image_extensions:
            image_file_filter = Gtk.FileFilter()
            image_file_filter.add_pixbuf_formats()
            image_file_filter.set_name(_("Images"))
            self._native.add_filter(image_file_filter)

        if self.use_custom_file_extensions:
            custom_file_filter = Gtk.FileFilter()
            for extension in self.custom_file_extensions:
                custom_file_filter.add_suffix(extension.lstrip().rstrip())
            custom_file_filter.set_name(_("Accepted files"))
            self._native.add_filter(custom_file_filter)

        # Signals and show dialog
        self._native.connect("response", self._on_open_response)
        self._native.show()

    def _on_open_response(self, dialog:Gtk.NativeDialog, response:int):
        if response == Gtk.ResponseType.ACCEPT:
            self._open_file(dialog.get_file())
        else:
            self._open_btn.set_sensitive(True)
            self._stack.set_visible_child_name(self._previous_view) # Restore previous view

        self._native = None

    def _open_file(self, file:Gio.File):
        file_path = file.peek_path()
        file_size = file.query_info("*", 0, None).get_size()

        if file_size > 536870912: # 512 Mb
            self._fileview.set_file_path(file_path)
            self._fileview.set_file_size(humanize.naturalsize(file_size))
            self._stack.set_visible_child_name("file-area") # Set view without saving the previous
            self.emit("big-file")
            self.emit("file-loaded")
            self._open_btn.set_sensitive(True)
            self._view_btn.set_visible(False)
        else:
            file.load_contents_async(None, self._open_file_async_complete)

    def _open_file_async_complete(self, source_file:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer=None):
        contents = source_file.load_contents_finish(result)
        if not contents[0]:
            self._stack.set_visible_child_name(self._previous_view)
            self.emit("error", f"Unable to open {source_file.peek_path()}: {contents[1]}.")
            return

        if Utils.is_text(contents[1]) and self.allow_drag_and_drop:
            text = contents[1].decode("utf-8")
            text_buffer = self._textview.get_buffer()
            text_buffer.set_text(text)
            text_buffer.place_cursor(text_buffer.get_end_iter())
            self._open_btn.set_sensitive(True)
            self._view_btn.set_visible(False)
            self._stack.set_visible_child_name("text-area") # Set view without saving the previous
            self.emit("text-changed")
        elif Utils.is_image(contents[1]) and self.allow_drag_and_drop:
            image_bytes = GLib.Bytes(contents[1])
            texture = Gdk.Texture.new_from_bytes(image_bytes)
            self._file_bytes = image_bytes
            self._fileview.set_file_path(source_file.peek_path())
            self._imageview.set_paintable(texture)
            self._open_btn.set_sensitive(True)
            self._view_btn.set_visible(True)
            self._stack.set_visible_child_name("image-area") # Set view without saving the previous
            self.emit("image-loaded")
        elif self.allow_drag_and_drop:
            self._file_bytes = contents[1]
            file_path = source_file.peek_path()
            file_size = source_file.query_info("*", 0, None).get_size()
            self._fileview.set_file_path(file_path)
            self._fileview.set_file_size(humanize.naturalsize(file_size))
            self._open_btn.set_sensitive(True)
            self._view_btn.set_visible(False)
            self._stack.set_visible_child_name("file-area") # Set view without saving the previous
            self.emit("file-loaded")

    def _on_save_clicked(self, user_data:GObject.GPointer):

        # Start loading animation and disable save button
        self._save_btn.set_sensitive(False)
        self._loading_lbl.set_label(_("Saving file..."))
        self.set_visible_view("loading")

        app = Gio.Application.get_default()
        window = app.get_active_window()
        self._native = Gtk.FileChooserNative(
            transient_for=window,
            title=_("Save file as"),
            action=Gtk.FileChooserAction.SAVE,
            accept_label=_("Save"),
            cancel_label=_("Cancel"),
        )
        self._native.connect("response", self._on_save_response)
        self._native.show()

    def _on_save_response(self, dialog:Gtk.NativeDialog, response:int):
        if response == Gtk.ResponseType.ACCEPT:
            self._save_file(dialog.get_file())
        else:
            self._save_btn.set_sensitive(True)
            self._stack.set_visible_child_name(self._previous_view)

        self._native = None

    def _save_file(self, file:Gio.File):

        # If there is nothing to save, return early
        if not self._file_bytes:
            return

        file.replace_contents_bytes_async(self._file_bytes, None, False, Gio.FileCreateFlags.NONE, None, self._on_save_file_complete)

    def _on_save_file_complete(self, source_file:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer=None):
        res = source_file.replace_contents_finish(result)
        file_path = source_file.peek_path()

        self._save_btn.set_sensitive(True)
        self._stack.set_visible_child_name(self._previous_view)
        if not res:
            self.emit("error", f"Unable to save {file_path}")
            return

        self.emit("saved", file_path)

    def _on_text_changed(self, data):
        self.emit("text-changed")

    def _clear(self):
        self._view_btn.set_visible(False)
        self._textview.get_buffer().set_text("")
        self._textview.remove_css_class("border-red")
        self._fileview.set_file_path("")
        self._fileview.set_file_size("")
        self._stack.set_visible_child_name("text-area")

    def get_text(self) -> str:
        text_buffer = self._textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), False)
        return text

    def set_text(self, text:str):
        self._textview.get_buffer().set_text(text, -1)

    def get_buffer(self) -> GtkSource.Buffer:
        return self._textview.get_buffer()

    def set_image(self, image_bytes:GLib.Bytes):
        self._imageview.set_paintable(Gdk.Texture.new_from_bytes(image_bytes))
        self._file_bytes = image_bytes

    def set_opened_file(self, file_bytes:List[bytes], file_path:str):
        self._file_bytes = file_bytes
        self._fileview.set_file_path(file_path)

    def set_opened_file_path(self, file_path:str):
        self._fileview.set_file_path(file_path)

    def get_opened_file_path(self) -> str:
        return self._fileview.get_file_path()

    def get_opened_file_size(self) -> str:
        return self._fileview.get_file_size()

    def add_css_class(self, css_class_name:str):
        self._textview.add_css_class(css_class_name)
        self._imageview.add_css_class(css_class_name)
        self._fileview.add_css_class(css_class_name)

    def remove_css_class(self, css_class_name:str):
        self._textview.remove_css_class(css_class_name)
        self._imageview.remove_css_class(css_class_name)
        self._fileview.remove_css_class(css_class_name)

    def get_visible_view(self) -> str:
        return self._stack.get_visible_child_name()

    def set_visible_view(self, view_name:str):
        self._previous_view = self._stack.get_visible_child_name()
        self._stack.set_visible_child_name(view_name)

    def set_text_language_highlight(self, language:str):
        self._textview.get_buffer().set_language(GtkSource.LanguageManager.get_default().get_language(language))

    def set_loading_visible(self, enabled:bool, label:str):
        if enabled:
            self.loading_lbl = label
            self._stack.set_visible_child_name("loading")
        else:
            self._stack.set_visible_child_name(self._previous_view)

    def set_spinner_spin(self, enabled: bool):
        self._spinner.set_visible(enabled)

    def clear(self):
        self._clear()
