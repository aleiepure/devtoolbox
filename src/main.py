# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Tuple

from .tools import TOOLS_METADATA
from .widgets.theme_switcher import ThemeSwitcher
from .widgets.image_area import ImageArea
from .widgets.webview_area import WebviewArea
from .widgets.entry_row import EntryRow
from .widgets.date_area import DateArea
from .widgets.spin_area import SpinArea
from .widgets.sidebar_item import SidebarItem
from .widgets.text_file_area import TextFileArea
from .widgets.file_view import FileView
from .widgets.text_area import TextArea
from .widgets.utility_title import UtilityTitle
from .window import DevtoolboxWindow
from .search_provider import DevToolboxSearchProvider
from gi.repository import Gtk, Gio, Adw, GObject, GtkSource, GLib
import sys
from pathlib import Path


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
        SpinArea,
        DateArea,
        EntryRow,
        WebviewArea,
        ImageArea,
        ThemeSwitcher,
    ]

    def __init__(self, version, debug):
        super().__init__(
            application_id="me.iepure.devtoolbox",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )

        self._version = version
        self._debug = debug

        self.add_main_option(
            'help',
            ord('h'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Show this help message",
            None
        )
        self.add_main_option(
            'version',
            ord('v'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Show version information",
            None
        )
        self.add_main_option(
            'list',
            ord('l'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "List available tools",
            None
        )
        self.add_main_option(
            'tool',
            ord('t'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "Open a specific tool",
            'TOOL_NAME'
        )
        self.add_main_option(
            'search',
            ord('s'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "Search for tools",
            'SEARCH_TERMS'
        )
        self.add_main_option(
            'search-provider',
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Run as search provider",
            None
        )

        self.create_action("quit", self.on_quit_action, ["<primary>q", "<primary>w"])
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
            win = DevtoolboxWindow(self._debug, application=self)
            win.connect("close-request", self._on_close_request)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        builder = Gtk.Builder.new_from_resource(
            "/me/iepure/devtoolbox/ui/about_dialog.ui")
        about_dialog = builder.get_object("about_dialog")

        if self._debug == "True":
            about_dialog.set_application_name(
                f"{about_dialog.get_application_name()}\n(Development snapshot)")
            about_dialog.set_application_icon("me.iepure.devtoolbox")

        about_dialog.set_version(self._version)
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
            "Konstantin Tutsch https://github.com/konstantintutsch",
            "Finnever https://github.com/MrFinnever",
            "Nyx https://github.com/nyx-4",
            "Christian Backes https://github.com/inpector",
            "twlvnn https://github.com/twlvnn",
            "Angelo Rafael https://github.com/lo2dev",
            "DJKnaeckebrot https://github.com/lo2dev",
            "Djalim Simaila https://github.com/DjalimSimaila",
            "TamilNeram https://github.com/TamilNeram",
            "Emilio Sepúlveda M. https://github.com/emisep",
            "Chris Heywood https://github.com/cheywood",
            "John Peter Sa https://github.com/johnpetersa19",
            "Nino678190 https://github.com/Nino678190",
            "Sebastian K. https://github.com/spktkpkt",
            "PonyLucky https://github.com/PonyLucky",
        ])
        about_dialog.present(self.props.active_window)

    def on_quit_action(self, widget, _):
        # Clean up temp files

        tmp_files = Path(GLib.get_tmp_dir()).glob('me.iepure.devtoolbox*')
        for tmp_file in tmp_files:
            tmp_file.unlink(missing_ok=True)
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

    def _on_close_request(self, user_data: GObject.GPointer):
        self.on_quit_action(None, None)

    def do_command_line(self, command_line):
        """Handle command line arguments from primary instance."""

        arguments = command_line.get_arguments()

        tool_name = None
        search_terms = None

        # Parse arguments
        i = 0
        while i < len(arguments):
            arg = arguments[i]
            if arg == '--tool' or arg == '-t':
                if i + 1 < len(arguments):
                    tool_name = arguments[i + 1]
                i += 2
            elif arg == '--search' or arg == '-s':
                if i + 1 < len(arguments):
                    search_terms = arguments[i + 1]
                i += 2
            elif arg == '--search-provider':
                return self._run_search_provider()
            else:
                i += 1

        # Always activate first to ensure window exists
        self.activate()
        window = self.get_active_window()

        if window:
            success = self._handle_parsed_args(tool_name, search_terms, window)

        return 0 if success else 1

    def _handle_parsed_args(self, tool_name, search_terms, window) -> bool:
        """Handle parsed command line arguments when window is ready."""

        if tool_name:
            if not window.open_tool(tool_name):
                print(f"Tool '{tool_name}' not found. Use '--list (-l)' to see available tools.")
                return False
            else:
                print(f"Opened tool: {tool_name}")
        elif search_terms:
            window.activate_search(search_terms)
            
        return True

    def do_local_command_line(self, arguments: List[str]) -> Tuple[bool, List[str], int]:
        """Handle command line arguments."""

        if '--help' in arguments or '-h' in arguments:
            arguments.remove('--help' if '--help' in arguments else '-h')
            print("Usage: devtoolbox [options]\n"
                  "Options:\n"
                  "  -h, --help                   Show this help message\n"
                  "  -v, --version                Show version information\n"
                  "  -l, --list                   List available tools\n"
                  "  -t, --tool <TOOL_NAME>       Open a specific tool\n"
                  "  -s, --search <SEARCH_TERMS>  Search for tools\n"
                  "  --search-provider            Run as search provider")
            return True, arguments, 0

        elif '--version' in arguments or '-v' in arguments:
            arguments.remove('--version' if '--version' in arguments else '-v')
            print(f"Devtoolbox version {self._version}")
            return True, arguments, 0

        elif '--list' in arguments or '-l' in arguments:
            arguments.remove('--list' if '--list' in arguments else '-l')
            print("Available tools:")
            for tool_id, tool_meta in TOOLS_METADATA.items():
                print(f"  {tool_id}: {tool_meta["title"]}")
            return True, arguments, 0

        elif '--search-provider' in arguments:
            try:
                arguments.remove('--search-provider')
                exit_status = self._run_search_provider()
                return True, arguments, exit_status
            except Exception as e:
                print(f"Search provider error: {e}")
                return True, arguments, 1

        # For all other arguments, let the primary instance handle them
        return False, arguments, 0

    def _run_search_provider(self):
        """Run the search provider."""
        try:
            print("Starting search provider...")
            search_provider = DevToolboxSearchProvider()
            return search_provider.run()
        except Exception as e:
            print(f"Search provider error: {e}")
            return 1


def main(version, debug):
    """The application's entry point."""
    app = DevtoolboxApplication(version, debug)
    return app.run(sys.argv)
