# application.py
#
# Copyright 2022 Alessandro Iepure
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw

from devtoolbox.window import MainWindow


class Application(Adw.Application):
    def __init__(self):
        Adw.Application.__init__(self, application_id='me.iepure.devtoolbox',
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        self.create_action('about', self.show_about_dialog)

    def on_quit_action(self, widget, _):
        self.quit()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def show_about_dialog(self, widget, _):
        builder = Gtk.Builder.new_from_resource("/me/iepure/devtoolbox/ui/about.ui")
        about_window = builder.get_object("about_window")
        about_window.set_transient_for(_)
        about_window.present()



def main(version):
    """The application's entry point."""
    app = Application()
    return app.run(sys.argv)
