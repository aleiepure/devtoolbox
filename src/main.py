# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GtkSource", "5")

from gi.repository import Gtk, Gio, Adw, GObject, GtkSource
from .window import DevtoolboxWindow
from .widgets.utility_title import UtilityTitle
from .widgets.text_area import TextArea
from .widgets.file_viewer import FileViewer
from .widgets.text_file_area import TextFileArea
from .widgets.text_field_action_row import TextFieldActionRow
from .widgets.sidebar_item import SidebarItem
from .widgets.binary_selector import BinarySelector
from .widgets.spin_area import SpinArea
from .widgets.date_area import DateArea
from .widgets.entry_row import EntryRow


class DevtoolboxApplication(Adw.Application):
    """The main application singleton class."""

    _custom_widgets = [
        GtkSource.View,
        GtkSource.Buffer,
        GtkSource.Completion,
        GtkSource.StyleScheme,
        UtilityTitle,
        TextArea,
        FileViewer,
        TextFileArea,
        TextFieldActionRow,
        SidebarItem,
        BinarySelector,
        SpinArea,
        DateArea,
        EntryRow,
    ]

    def __init__(self, version, debug):
        super().__init__(
            application_id="me.iepure.devtoolbox", flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.version = version
        self.debug = debug
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)

        self.create_action("quit", self.quit, ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)

        # Register custom types
        for i in self._custom_widgets:
            GObject.type_ensure(i)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = DevtoolboxWindow(self.debug, application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        builder = Gtk.Builder.new_from_resource(
            "/me/iepure/devtoolbox/ui/about_window.ui"
        )
        about_window = builder.get_object("about_window")
        if self.debug == "True":
            about_window.set_application_name(
                f"{about_window.get_application_name()}\n(Development snapshot)"
            )
            about_window.set_icon_name("me.iepure.devtoolbox")
        about_window.set_version(self.version)
        about_window.set_transient_for(self.props.active_window)
        about_window.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print("app.preferences action activated")

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version, debug):
    """The application's entry point."""
    app = DevtoolboxApplication(version, debug)
    return app.run(sys.argv)
