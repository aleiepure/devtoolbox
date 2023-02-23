# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GtkSource, Gdk
from gettext import gettext as _
import humanize

from devtoolbox.utils import Utils


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/widgets/text_area.ui")
class TextArea(Adw.Bin):
    __gtype_name__ = "TextArea"

    # Template elements
    _name_lbl = Gtk.Template.Child()
    _spinner = Gtk.Template.Child()
    _spinner_separator = Gtk.Template.Child()
    _action_btn = Gtk.Template.Child()
    _action_btn_separator = Gtk.Template.Child()
    _open_btn = Gtk.Template.Child()
    _copy_btn = Gtk.Template.Child()
    _paste_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()
    _textview = Gtk.Template.Child()
    _stack = Gtk.Template.Child()
    _loading_lbl = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    # Properties
    name = GObject.Property(type=str, default="")
    show_spinner = GObject.Property(type=bool, default=False)
    show_clear_btn = GObject.Property(type=bool, default=False)
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
        "big-file": (GObject.SIGNAL_RUN_LAST, None, ()),
        "cursor-moved": (GObject.SIGNAL_RUN_LAST, None, ()),
        "error": (GObject.SIGNAL_RUN_LAST, None, (str,)),
    }

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "textarea")

        # Set theme
        language = GtkSource.LanguageManager.get_default().get_language(self.text_language_highlight)
        style_from_settings = self._settings.get_string("style-scheme")
        style_scheme = (GtkSource.StyleSchemeManager().get_default().get_scheme(style_from_settings))
        self._textview.get_buffer().set_language(language)
        self._textview.get_buffer().set_style_scheme(style_scheme)

        # Drag and drop
        content = Gdk.ContentFormats.new_for_gtype(Gdk.FileList)
        target = Gtk.DropTarget(formats=content, actions=Gdk.DragAction.COPY)
        target.connect("drop", self._on_dnd_drop)
        self._textview.add_controller(target)

        # Property binding
        self.bind_property("name", self._name_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner_separator, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-clear-btn", self._clear_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-copy-btn", self._copy_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-open-btn", self._open_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
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
        self._clear_btn.connect("clicked", self._on_clear_clicked)
        self._copy_btn.connect("clicked", self._on_copy_clicked)
        self._paste_btn.connect("clicked", self._on_paste_clicked)
        self._open_btn.connect("clicked", self._on_open_clicked)
        self._text_changed_handler = self._textview.get_buffer().connect("changed", self._on_text_changed)
        self._textview.get_buffer().connect("cursor-moved", self._on_cursor_moved)

    def _on_dnd_drop(self, drop_target:Gtk.DropTarget, value: Gdk.FileList, x:float, y:float, user_data:GObject.Object=None):
        self._spinner.set_visible(True)
        files: List[Gio.File] = value.get_files()
        if len(files) != 1:
            self.emit("error", "Cannot open more than one file")
            return
        self._open_file(files[0])
        self._spinner.set_visible(False)

    def _on_action_clicked(self, user_data:GObject.GPointer):
        self.emit("action-clicked")

    def _on_clear_clicked(self, user_data:GObject.GPointer):
        self._clear()
        self.emit("view-cleared")

    def _on_copy_clicked(self, user_data:GObject.GPointer):
        text_buffer = self._textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), False)
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)
        self._stack.set_visible_child_name("text-area")

    def _on_paste_clicked(self, user_data:GObject.GPointer):
        text_buffer = self._textview.get_buffer()
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        text_buffer.paste_clipboard(clipboard, None, True)
        self._stack.set_visible_child_name("text-area")

    def _on_open_clicked(self, user_data:GObject.GPointer):

        # Start loading animation and disable button
        self._open_btn.set_sensitive(False)
        self._stack.set_visible_child_name("loading")

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
        if self.use_default_text_extensions:
            text_file_filter = Gtk.FileFilter()
            text_file_filter.add_mime_type("text/*")
            text_file_filter.set_name(_("Text files"))
            self._native.add_filter(text_file_filter)

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
            self._stack.set_visible_child_name("text-area")

        self._native = None

    def _open_file(self, file:Gio.File):
        file_size = file.query_info("*", 0, None).get_size()

        if file_size > 536870912: # 512 Mb
            self._stack.set_visible_child_name("loading")
            self.loading_label = f"Loading a large file ({humanize.naturalsize(file_size)})\nMight take a while, please wait..."
            self.emit("big-file")
        file.load_contents_async(None, self._open_file_async_complete)

    def _open_file_async_complete(self, source_file:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer=None):
        contents = source_file.load_contents_finish(result)
        if not contents[0]:
            self.emit("error", f"Unable to open {source_file.peek_path()}: {contents[1]}.")
            return

        if Utils.is_text(contents[1]) and self.allow_drag_and_drop:
            text = contents[1].decode("utf-8")
            text_buffer = self._textview.get_buffer()
            text_buffer.set_text(text)
            text_buffer.place_cursor(text_buffer.get_end_iter())
            self._open_btn.set_sensitive(True)
            self._stack.set_visible_child_name("text-area")
            self.emit("text-loaded")
        elif self.allow_drag_and_drop:
            self._textview.get_buffer().set_text("")
            self._open_btn.set_sensitive(True)
            self._stack.set_visible_child_name("text-area")
            self.emit("error", "File is not UTF-8 encoded.")

    def _on_text_changed(self, user_data:GObject.GPointer):
        self.emit("text-changed")

    def _clear(self):
        self._textview.get_buffer().set_text("")
        self._textview.remove_css_class("border-red")
        self._stack.set_visible_child_name("text-area")
        self._spinner.set_visible(False)

    def _on_cursor_moved(self, user_data:GObject.GPointer):
        self.emit("cursor-moved")

    def get_text(self) -> str:
        text_buffer = self._textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), False)
        return text

    def set_text(self, text:str):
        self._textview.get_buffer().set_text(text)

    def get_buffer(self) -> GtkSource.Buffer:
        return self._textview.get_buffer()

    def set_buffer(self, buffer:GtkSource.Buffer):
        return self._textview.set_buffer(buffer)

    def add_css_class(self, css_class_name:str):
        self._textview.add_css_class(css_class_name)

    def remove_css_class(self, css_class_name:str):
        self._textview.remove_css_class(css_class_name)

    def get_visible_view(self) -> str:
        return self._stack.get_visible_child_name()

    def set_visible_view(self, view_name:str):
        self._previous_view = self._stack.get_visible_child_name()
        self._stack.set_visible_child_name(view_name)

    def set_text_language_highlight(self, language:str):
        self.text_language_highlight = language
        self._textview.get_buffer().set_language(GtkSource.LanguageManager.get_default().get_language(self.text_language_highlight))

    def set_loading_visible(self, enabled:bool, label:str):
        if enabled:
            self.loading_lbl = label
            self._stack.set_visible_child_name("loading")
        else:
            self._stack.set_visible_child_name("text-area")

    def set_spinner_spin(self, enabled: bool):
        self.show_spinner = enabled

    def clear(self):
        self._clear()

    def scroll_mark_onscreen(self, mark:Gtk.TextMark):
        self._textview.scroll_mark_onscreen(mark)

    def get_iter_at_location(self, x, y):
        return self._textview.get_iter_at_location(x,y)
