import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw, GLib

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'testt'
        self.props.version = "0.1.0"
        self.props.authors = ['Alessandro Iepure']
        self.props.copyright = '2022 Alessandro Iepure'
        self.props.logo_icon_name = 'me.iepure.devtoolbox'
        self.props.modal = True
        self.set_transient_for(parent)