# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GLib
from gettext import gettext as _

from .widgets.sidebar_item import SidebarItem
from .widgets.theme_switcher import ThemeSwitcher

from .tools import get_tools_for_ui, search_tools


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/window.ui")
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = "DevtoolboxWindow"

    # Template elements
    _split_view = Gtk.Template.Child()
    _show_search_btn = Gtk.Template.Child()
    _search_bar = Gtk.Template.Child()
    _search_entry = Gtk.Template.Child()
    _fav_btn = Gtk.Template.Child()
    _fav_stack = Gtk.Template.Child()
    _favorites = Gtk.Template.Child()
    _sidebar = Gtk.Template.Child()
    _toggle_sidebar_btn = Gtk.Template.Child()
    _show_sidebar_btn = Gtk.Template.Child()
    _menu_btn = Gtk.Template.Child()
    _content_stack = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def _toggle_search(self, new_state: GLib.Variant, source: Gtk.Widget) -> None:
        """
        Callback for the win.search action

        Args:
            new_state (bool): new selected state
            source (Gtk.Widget): widget that caused the activation

        Returns:
            None
        """

        source._search_bar.set_search_mode(new_state.get_boolean())
        source._show_search_btn.set_active(new_state.get_boolean())
        self.set_state(new_state)

    def _refresh_favorites(self, new_state: None, source: Gtk.Widget) -> None:
        """
        Callback for the win.search action

        Args:
            new_state (None): stateless action, always None
            source (Gtk.Widget): widget that caused the activation

        Returns:
            None
        """

        source._populate_favorites()

    _actions = {
        ('search', None, None, 'false', _toggle_search),
        ('refresh-favorites', _refresh_favorites)
    }

    def __init__(self, debug, **kwargs):
        super().__init__(**kwargs)

        self.add_action_entries(self._actions, self)

        # Theme (Adapted from https://gitlab.gnome.org/tijder/blueprintgtk/)
        self._menu_btn.get_popover().add_child(ThemeSwitcher(), "themeswitcher")
        if debug == "False":
            self.remove_css_class("devel")

        self._tools = get_tools_for_ui()

        # Populate sidebar and content stack
        for t in self._tools:
            self._sidebar.append(SidebarItem(
                tool_name=t,
                title=self._tools[t]["title"],
                icon_name=self._tools[t]["icon-name"],
                tool_tip=self._tools[t]["tooltip"],
                category=self._tools[t]["category"]))
            self._content_stack.add_named(self._tools[t]["child"], t)

        self._sidebar.set_header_func(
            self._create_sidebar_headers, None, None)
        self._sidebar.set_filter_func(self._filter_func, None, None)

        # Populate favorites
        self._populate_favorites()
        if self._favorites.get_row_at_index(0) is not None:
            self._fav_stack.set_visible_child_name("filled")

        # Select row for visible content
        try:
            index = list(self._tools.keys()).index(
            self._settings.get_string("last-tool"))
            if index == 0:
                self._sidebar.select_row(self._sidebar.get_first_child())
            else:
                self._sidebar.select_row(
                    self._sidebar.get_row_at_index(index))
        except ValueError:
            self._sidebar.select_row(self._sidebar.get_first_child())

        # Restore last state
        self._settings.bind("window-width", self,
            "default-width", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-height", self,
            "default-height", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-maximized", self,
            "maximized", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("sidebar-open", self._toggle_sidebar_btn,
            "active", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("last-tool", self._content_stack,
            "visible-child-name", Gio.SettingsBindFlags.DEFAULT)
        
        self.create_action("show-menu", self._on_show_menu_action, ["F10"])

    @Gtk.Template.Callback()
    def _on_favorite_row_activated(self, list_box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        """
        Callback for "row-activated" signal.
        Changes visible view and the selected row in the sidebar, closes the popover and the sidebar if the window is too small.

        Args:
            list_box (Gtk.ListBox): ListBox interracted with
            row (Gtk.ListBoxRow): selected row in ListBox

        Returns:
            None
        """

        self._content_stack.set_visible_child_name(row.get_tool_name())

        idx = 0
        sidebar_row = self._sidebar.get_row_at_index(idx)
        while sidebar_row is not None:
            if row.get_tool_name() == sidebar_row.get_tool_name():
                self._sidebar.select_row(sidebar_row)
                self._sidebar.grab_focus()
                break
            idx += 1
            sidebar_row = self._sidebar.get_row_at_index(idx)

        self._fav_btn.popdown()
        if not self._toggle_sidebar_btn.get_visible():
            self._split_view.set_show_sidebar(False)

    @Gtk.Template.Callback()
    def _on_sidebar_row_activated(self, list_box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        """
        Callback for "row-activated" signal.
        Changes visible view and closes sidebar if the window is too small.

        Args:
            list_box (Gtk.ListBox): ListBox interracted with
            row (Gtk.ListBoxRow): selected row in ListBox

        Returns:
            None
        """

        self._content_stack.set_visible_child_name(row.get_tool_name())

        # Toggle not visible? => sidebar over content, close on selection
        if not self._toggle_sidebar_btn.get_visible():
            self._split_view.set_show_sidebar(False)

    @Gtk.Template.Callback()
    def _on_map(self, user_data: object | None) -> None:
        """
        Callback for "map" signal.
        Grab sidebar focus to move scrolled window where the selected row is visible and immediately change focus to the
        tool in use.

        Args:
            user_data (object or None): additional data passed to the callback

        Returns:
            None
        """

        self._sidebar.grab_focus()
        self._content_stack.get_visible_child().grab_focus()

    @Gtk.Template.Callback()
    def _on_sidebar_btn_clicked(self, user_data: object | None) -> None:
        """
        Callback for "clicked" signal.
        Shows the sidebar.

        Args:
            user_data (object or None): additional data passed to the callback

        Returns:
            None
        """

        self._split_view.set_show_sidebar(True)

    def _create_sidebar_headers(self, row: Gtk.ListBoxRow, before: Gtk.ListBoxRow, user_data: object | None, dummy: None) -> None:
        """
        Creates the sidebar headers to separate the categories. Loops on every sidebar item.

        Args:
            row (Gtk.ListBoxRow): list box analyzed
            before (Gtk.ListBoxRow): list box preceding `row`
            user_data (object or None): additional data passed to the callback
            dummy (None): required variable to make function work (why?)

        Returns:
            None
        """

        if before is None or before.get_category() != row.get_category():
            header_label= Gtk.Label(label=row.get_category())
            header_label.set_halign(Gtk.Align.START)
            header_label.set_valign(Gtk.Align.CENTER)
            header_label.add_css_class("heading")
            header_label.add_css_class("dimmed")
            header_label.set_margin_start(12)
            header_label.set_margin_bottom(6)

            if before:
                header_label.set_margin_top(16)

            row.set_header(header_label)

    @ Gtk.Template.Callback()
    def _on_searchentry_search_changed(self, user_data: object | None) -> None:
        """
        Callback for "search-changed" signal.
        Invalidates filter to perform search.

        user_data (object or None): additional data passed to the callback
            dummy (None): required variable to make function work (why?)

        Returns:
            None
        """

        self._sidebar.invalidate_filter()

    def _filter_func(self, row: Gtk.ListBoxRow, user_data: object | None, dummy: None) -> bool:
        """
        Uses the shared search function to filter the sidebar items based on the search query.
        """

        search_query= self._search_entry.get_text()
        if not search_query:
            return True

        results = search_tools([search_query])
        return row.get_tool_name() in results

    def _populate_favorites(self) -> None:
        """
        Populates the favorites popover with the currrent gsettings values.

        Args:
            None

        Returns:
            None
        """

        self._favorites.remove_all()

        favorite_tools= self._settings.get_strv('favorites')
        if len(favorite_tools) == 0:
            self._fav_stack.set_visible_child_name('empty')
        else:
            self._fav_stack.set_visible_child_name('filled')
            for t in self._tools:
                if t in favorite_tools:
                    self._favorites.append(
                                SidebarItem(
                                        tool_name=t,
                                        title=self._tools[t]["title"],
                                        icon_name=self._tools[t]["icon-name"],
                                        tool_tip=self._tools[t]["tooltip"],
                                        category=self._tools[t]["category"]
                                    )
                                )

    def open_tool(self, tool_name: str) -> bool:
        """
        Public method to open a specific tool.
        Returns True if tool exists and was opened.
        """

        if tool_name not in self._tools:
            return False
            
        self._content_stack.set_visible_child_name(tool_name)
        
        # Select corresponding sidebar row
        idx = 0
        sidebar_row = self._sidebar.get_row_at_index(idx)
        while sidebar_row is not None:
            if tool_name == sidebar_row.get_tool_name():
                self._sidebar.select_row(sidebar_row)
                break
            idx += 1
            sidebar_row = self._sidebar.get_row_at_index(idx)
        
        return True
    
    def activate_search(self, search_terms: str = "") -> None:
        """
        Public method to activate search with optional terms.
        """
    
        
        self._search_bar.set_search_mode(True)
        self._show_search_btn.set_active(True)
        if search_terms:
            self._search_entry.set_text(search_terms)
        self._search_entry.grab_focus()

    def _on_show_menu_action(self, action: Gio.SimpleAction, param: GLib.Variant | None) -> None:
        """ Callback for the "show-menu" action. """
        
        self._menu_btn.popup()
        
    def create_action(self, name: str, callback: callable, accelerators: list[str] | None = None) -> None:
        """
        Creates a new action and adds it to the application.

        Args:
            name (str): Name of the action
            callback (callable): Function to call when the action is activated
            accelerators (list[str] | None): List of accelerators for the action

        Returns:
            None
        """
        
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if accelerators:
            app = self.get_application()
            action_name = f"win.{name}"
            app.set_accels_for_action(action_name, accelerators)
