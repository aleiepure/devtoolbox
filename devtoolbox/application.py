# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version('GtkSource', '5')
from gi.repository import Gtk, Gio, Adw, GObject, GtkSource

from devtoolbox.window import MainWindow
from devtoolbox.widgets.utility_title import UtilityTitle
from devtoolbox.widgets.text_area import TextArea
from devtoolbox.widgets.text_image_area import TextImageArea
from devtoolbox.widgets.text_image_file_area import TextImageFileArea
from devtoolbox.widgets.textfield_action_row import TextFieldActionRow


class Application(Adw.Application):

    custom_widgets = [
        GtkSource.View,
        GtkSource.Buffer,
        GtkSource.Completion,
        GtkSource.StyleScheme,
        UtilityTitle,
        TextArea,
        TextImageArea,
        TextImageFileArea,
        TextFieldActionRow,
    ]

    def __init__(self, version):
        Adw.Application.__init__(self, application_id="me.iepure.devtoolbox",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.version = version
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)

        # Register custom types
        for i in self.custom_widgets:
            GObject.type_ensure(i)

        # Actions
        self.create_action("quit", self.on_quit_action, ["<primary>q"])
        self.create_action("about", self.show_about_dialog)

    def on_quit_action(self, widget, _):
        self.quit()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.set_title("Dev Toolbox")
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def show_about_dialog(self, widget, _):
        builder = Gtk.Builder.new_from_resource(
            "/me/iepure/devtoolbox/ui/about_window.ui")
        about_window = builder.get_object("about_window")
        about_window.set_version(self.version)
        about_window.set_transient_for(_)
        about_window.present()


def main(version):
    """The application's entry point."""
    app = Application(version)
    return app.run(sys.argv)
