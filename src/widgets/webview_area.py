# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, GtkSource, Gdk, WebKit2
from gettext import gettext as _


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/widgets/webview_area.ui")
class WebviewArea(Adw.Bin):
    __gtype_name__ = "WebviewArea"

    # Template elements
    _box = Gtk.Template.Child()
    _name_lbl = Gtk.Template.Child()
    _spinner = Gtk.Template.Child()
    _spinner_separator = Gtk.Template.Child()

    _webview = WebKit2.WebView()

    # Properties
    name = GObject.Property(type=str, default="")
    show_spinner = GObject.Property(type=bool, default=False)

    _blank_html = '<html><body style="color-scheme: dark;background-color: #0d1117;"></body></html>'

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "webarea")

        # Style and add webview
        self._webview.set_vexpand(True)
        self._webview.set_hexpand(True)
        self._webview.set_margin_bottom(3)
        self._webview.set_margin_start(3)
        self._webview.set_margin_end(3)
        # self._webview.add_css_class("padding-5")
        self._webview.load_html(self._blank_html, "")
        self._box.append(self._webview)

        # Property binding
        self.bind_property("name", self._name_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner_separator, "visible", GObject.BindingFlags.SYNC_CREATE)
        self._spinner.bind_property("spinning", self._spinner, "visible", GObject.BindingFlags.BIDIRECTIONAL)
        self._spinner.bind_property("visible", self._spinner_separator, "visible", GObject.BindingFlags.BIDIRECTIONAL)

        # Signals
        self._webview.connect("decide-policy", self._on_policy_decision)
        self._webview.connect("context_menu", self._disable_contex_menu)

    def _on_policy_decision(self, webview:WebKit2.WebView, decision:WebKit2.NavigationPolicyDecision, decision_type:WebKit2.PolicyDecisionType):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            uri = decision.get_navigation_action().get_request().get_uri()
            if decision.get_navigation_action().is_user_gesture() and not uri.split("#")[0] == webview.get_uri():
                decision.ignore()
                app = Gio.Application.get_default()
                window = app.get_active_window()
                Gtk.show_uri(window, uri, Gdk.CURRENT_TIME)

    def _disable_contex_menu(self, web_view:WebKit2.WebView, context_menu:WebKit2.ContextMenu, event:Gdk.Event, hit_test_result:WebKit2.HitTestResult):
        return True

    def load_uri(self, uri:str):
        self._webview.load_uri(uri)
