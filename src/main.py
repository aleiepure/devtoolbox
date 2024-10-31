# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GtkSource", "5")
gi.require_version('WebKit', '6.0')
gi.require_version('Gcr', '4')

from gi.repository import Gtk, Gio, Adw, GObject, GtkSource, Gdk

from .window import DevtoolboxWindow

from .widgets.utility_title import UtilityTitle
from .widgets.text_area import TextArea
from .widgets.file_view import FileView
from .widgets.text_file_area import TextFileArea
from .widgets.sidebar_item import SidebarItem
from .widgets.binary_selector import BinarySelector
from .widgets.spin_area import SpinArea
from .widgets.date_area import DateArea
from .widgets.entry_row import EntryRow
from .widgets.webview_area import WebviewArea
from .widgets.image_area import ImageArea
from .widgets.theme_switcher import ThemeSwitcher


class DevtoolboxApplication(Adw.Application):
    """The main application class"""

    _custom_widgets = [
        GtkSource.View,
        GtkSource.Buffer,
        GtkSource.Completion,
        GtkSource.StyleScheme,
        UtilityTitle,
        TextArea,
        FileView,
        TextFileArea,
        SidebarItem,
        BinarySelector,
        SpinArea,
        DateArea,
        EntryRow,
        WebviewArea,
        ImageArea,
        ThemeSwitcher,
    ]

    def __init__(self, version, debug):
        super().__init__(application_id="me.iepure.devtoolbox", flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.version = version
        self.debug = debug
        # Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)

        self.create_action("quit", self.on_quit_action, ["<primary>q"])
        self.create_action("about", self.on_about_action)

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
        builder = Gtk.Builder.new_from_resource("/me/iepure/devtoolbox/ui/about_dialog.ui")
        about_dialog = builder.get_object("about_dialog")
        
        if self.debug == "True":
            about_dialog.set_application_name(f"{about_dialog.get_application_name()}\n(Development snapshot)")
            about_dialog.set_application_icon("me.iepure.devtoolbox")
        
        about_dialog.set_version(self.version)
        about_dialog.add_credit_section("Contributors", [
            "Rafael Fontenelle https://github.com/rffontenelle",
            "Sabri Ünal https://github.com/sabriunal",
            "Allan Nordhøy https://github.com/comradekingu",
            "Silvério Santos https://github.com/SantosSi",
            "gallegonovato https://github.com/gallegonovato",
            "Amerey https://github.com/Amereyeu",
            "gregorni https://github.com/gregorni",
            "Óscar Fernández Díaz <oscfdezdz@tuta.io>",
            "Hari Rana https://github.com/TheEvilSkeleton",
            "K.B.Dharun Krishna https://github.com/kbdharun",
            "L.Yang <yang120120110@gmail.com>",
            "Finnever https://github.com/MrFinnever",
            "Miyu Sakatsuki https://github.com/Miyu-dev",
            "复予 https://github.com/CloneWith",
            "Konstantin Tutsch https://github.com/konstantintutsch",
            "Zishan Rahman https://github.com/Zishan-Rahman",
            "Mariana Batista https://github.com/maahbatistaa",
            "SuperAtraction https://github.com/SuperAtraction",
            "Claudio https://github.com/K-eL",
            "mthw0 https://github.com/mthw0",
            "Ismael Brendo https://github.com/Ismaelbrendo",
            "Amer Sawan https://github.com/amersaw",
        ])
        about_dialog.present(self.props.active_window)

    def on_quit_action(self, widget, _):
        self.quit()

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
