# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GtkSource, Gdk, GLib
from gettext import gettext as _
from typing import List


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/image_area.ui')
class ImageArea(Adw.Bin):
    __gtype_name__ = "ImageArea"

    # Template elements
    _name_lbl = Gtk.Template.Child()
    _view_btn = Gtk.Template.Child()
    _open_btn = Gtk.Template.Child()
    _save_btn = Gtk.Template.Child()
    _clear_btn = Gtk.Template.Child()
    _stack = Gtk.Template.Child()
    _imageview = Gtk.Template.Child()
    _loading_lbl = Gtk.Template.Child()

    # Properties
    name = GObject.Property(type=str, default="Original")
    show_view_btn = GObject.Property(type=bool, default=False)
    show_clear_btn = GObject.Property(type=bool, default=False)
    show_save_btn = GObject.Property(type=bool, default=False)
    show_open_btn = GObject.Property(type=bool, default=False)
    loading_label = GObject.Property(type=str, default="Opening file...")
    allow_drag_and_drop = GObject.Property(type=bool, default=False)

    # Custom signals
    __gsignals__ = {
        "view-cleared": (GObject.SIGNAL_RUN_LAST, None, ()),
        "image-loaded": (GObject.SIGNAL_RUN_LAST, None, ()),
        "error": (GObject.SIGNAL_RUN_LAST, None, (str,)),
        "saved": (GObject.SIGNAL_RUN_LAST, None, (str,)),
    }

    def __init__(self):
        super().__init__()

        # Drag and drop
        content = Gdk.ContentFormats.new_for_gtype(Gdk.FileList)
        target = Gtk.DropTarget(formats=content, actions=Gdk.DragAction.COPY)
        target.connect('drop', self._on_dnd_drop)
        self._imageview.add_controller(target)

        # Property binding
        self.bind_property("name", self._name_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-view-btn", self._view_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-clear-btn", self._clear_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-open-btn", self._open_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-save-btn", self._save_btn, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("loading-label", self._loading_lbl, "label", GObject.BindingFlags.SYNC_CREATE)

        # Signals
        self._view_btn.connect("clicked", self._on_view_clicked)
        self._clear_btn.connect("clicked", self._on_clear_clicked)
        self._open_btn.connect("clicked", self._on_open_clicked)
        self._save_btn.connect("clicked", self._on_save_clicked)

    def _on_dnd_drop(self, drop_target:Gtk.DropTarget, value: Gdk.FileList, x:float, y:float, user_data:GObject.Object=None):
        files: List[Gio.File] = value.get_files()
        if len(files) != 1:
            self.emit("error", "Cannot open more than one file")
            return
        self._open_file(files[0])

    def _on_view_clicked(self, user_data:GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        Gtk.show_uri(window, self._imageview.get_file().get_uri(), Gdk.CURRENT_TIME)

    def _on_clear_clicked(self, user_data:GObject.GPointer):
        self._clear()
        self._open_btn.set_sensitive(True)
        self.emit("view-cleared")

    def _on_open_clicked(self, user_data:GObject.GPointer):

        # Start loading animation and disable open button
        self._open_btn.set_sensitive(False)
        self._stack.set_visible_child_name("loading")
        self.loading_label = _("Opening image...")

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
        image_file_filter = Gtk.FileFilter()
        image_file_filter.add_pixbuf_formats()
        image_file_filter.set_name(_("Images"))
        self._native.add_filter(image_file_filter)

        # Signals and show dialog
        self._native.connect("response", self._on_open_response)
        self._native.show()

    def _on_open_response(self, dialog:Gtk.NativeDialog, response:int):
        if response == Gtk.ResponseType.ACCEPT:
            self._open_file(dialog.get_file())
        else:
            self._open_btn.set_sensitive(True)
            self._stack.set_visible_child_name("image")

        self._native = None

    def _open_file(self, file:Gio.File):
        if file and self.allow_drag_and_drop:
            self._imageview.set_file(file)
            self._view_btn.set_visible(True)
            self.emit("image-loaded")

        self._open_btn.set_sensitive(True)
        self._stack.set_visible_child_name("image")

    def _on_save_clicked(self, user_data:GObject.GPointer):

        # Start loading animation and disable save button
        self._save_btn.set_sensitive(False)
        self.loading_label = _("Saving image...")
        self._stack.set_visible_child_name("loading")

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
            self._stack.set_visible_child_name("image")

        self._native = None

    def _save_file(self, destination:Gio.File):
        self._imageview.get_file().copy_async(destination, Gio.FileCopyFlags.NONE, 0, None, None, None, self._on_save_file_complete, None)

    def _on_save_file_complete(self, file:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer=None):
        res = file.copy_finish(result)

        self._save_btn.set_sensitive(True)
        self._stack.set_visible_child_name("image")
        if not res:
            self.emit("error", _("Unable to save image."))
            return

        self.emit("saved", file.get_path())

    def _clear(self):
        self._view_btn.set_visible(False)
        self._save_btn.set_visible(False)
        self._stack.set_visible_child_name("image")
        self._imageview.set_file(None)

    def set_file(self, file:Gio.File):
        self._imageview.set_file(file)

    def clear(self):
        self._clear()

    def set_file(self, file:Gio.File):
        self._view_btn.set_visible(True)
        self._save_btn.set_visible(True)
        self._imageview.set_file(file)

    def get_file(self) -> Gio.File:
        return self._imageview.get_file()

    def set_visible_view(self, view_name:str):
        self._stack.set_visible_child_name(view_name)

    def set_loading_lbl(self, loading_lbl:str):
        self.loading_label = loading_lbl
