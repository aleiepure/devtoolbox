# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GLib, GObject
import subprocess
import time
from typing import List, Dict, Any
from .tools import TOOLS_METADATA, search_tools


class DevToolboxSearchProvider(GObject.Object):
    """GNOME Shell search provider for Dev Toolbox."""

    IDLE_TIMEOUT = 10  # 30 seconds of inactivity
    CACHE_DURATION = 300  # 5 minutes

    def __init__(self):
        super().__init__()
        self._search_cache = {}
        self._cache_timestamps = {}
        self._bus = None
        self._registration_id = None
        self._idle_timeout_id = None
        self._main_loop = None

        # D-Bus interface
        self.interface_xml = """
        <node>
            <interface name="org.gnome.Shell.SearchProvider2">
                <method name="GetInitialResultSet">
                    <arg type="as" name="terms" direction="in" />
                    <arg type="as" name="results" direction="out" />
                </method>
                <method name="GetSubsearchResultSet">
                    <arg type="as" name="previous_results" direction="in" />
                    <arg type="as" name="terms" direction="in" />
                    <arg type="as" name="results" direction="out" />
                </method>
                <method name="GetResultMetas">
                    <arg type="as" name="identifiers" direction="in" />
                    <arg type="aa{sv}" name="metas" direction="out" />
                </method>
                <method name="ActivateResult">
                    <arg type="s" name="identifier" direction="in" />
                    <arg type="as" name="terms" direction="in" />
                    <arg type="u" name="timestamp" direction="in" />
                </method>
                <method name="LaunchSearch">
                    <arg type="as" name="terms" direction="in" />
                    <arg type="u" name="timestamp" direction="in" />
                </method>
            </interface>
        </node>
        """

    def _reset_idle_timer(self):
        """Reset the idle timeout timer"""
        
        # Cancel existing timer
        if self._idle_timeout_id:
            GLib.source_remove(self._idle_timeout_id)
        
        # Start new timer
        self._idle_timeout_id = GLib.timeout_add_seconds(
            self.IDLE_TIMEOUT, 
            self._on_idle_timeout
        )
        
        print(f"DEBUG: Reset idle timer to {self.IDLE_TIMEOUT} seconds")

    def _on_idle_timeout(self):
        """Called when idle timeout expires"""
        
        print("DEBUG: Idle timeout reached, shutting down search provider...")
        if self._main_loop:
            self._main_loop.quit()
        return False  # No repeat

    def _search_with_cache(self, terms: List[str]) -> List[str]:
        """Search with caching for performance"""

        cache_key = '|'.join(sorted(terms))
        current_time = time.time()

        # Check cache
        if (cache_key in self._search_cache and
            cache_key in self._cache_timestamps and
                current_time - self._cache_timestamps[cache_key] < self.CACHE_DURATION):
            print(f"DEBUG: Cache hit for: {cache_key}")
            return self._search_cache[cache_key]

        # Perform search
        results = search_tools(terms)[:8]  # Limit to 8 results for GNOME Shell
        print(f"DEBUG: Search results for '{' '.join(terms)}': {results}")

        # Cache results
        self._search_cache[cache_key] = results
        self._cache_timestamps[cache_key] = current_time

        # Cleanup old cache entries
        self._cleanup_cache(current_time)

        return results

    def _cleanup_cache(self, current_time: float):
        """Remove old cache entries"""

        expired_keys = [
            key for key, timestamp in self._cache_timestamps.items()
            if current_time - timestamp >= self.CACHE_DURATION
        ]
        for key in expired_keys:
            self._search_cache.pop(key, None)
            self._cache_timestamps.pop(key, None)

    def GetInitialResultSet(self, terms: List[str]) -> List[str]:
        """GNOME Shell SearchProvider2 interface method"""

        print(f"DEBUG: GetInitialResultSet called with: {terms}")
        self._reset_idle_timer()
        return self._search_with_cache(terms)

    def GetSubsearchResultSet(self, previous_results: List[str], terms: List[str]) -> List[str]:
        """GNOME Shell SearchProvider2 interface method"""

        print(f"DEBUG: GetSubsearchResultSet called with: {terms}")
        self._reset_idle_timer()
        return self._search_with_cache(terms)

    def GetResultMetas(self, identifiers: List[str]) -> List[Dict[str, Any]]:
        """GNOME Shell SearchProvider2 interface method"""

        print(f"DEBUG: GetResultMetas called with: {identifiers}")
        self._reset_idle_timer()
        
        metas = []
        for tool_id in identifiers:
            if tool_id in TOOLS_METADATA:
                tool = TOOLS_METADATA[tool_id]

                meta = {
                    'id': GLib.Variant('s', tool_id),
                    'name': GLib.Variant('s', tool['title']),
                    'description': GLib.Variant('s', tool['tooltip']),
                }
                metas.append(meta)
                print(f"DEBUG: Added meta for {tool_id}: {tool['title']}")
        return metas

    def ActivateResult(self, identifier: str, terms: List[str], timestamp: int):
        """GNOME Shell SearchProvider2 interface method"""

        print(
            f"DEBUG: ActivateResult called - tool: {identifier}, terms: {terms}")
        self._reset_idle_timer()
        
        # Launch app with specific tool
        try:
            subprocess.run(
                [
                    '/app/bin/devtoolbox',
                    '--tool', identifier
                ],
                check=True,
            )

        except Exception as e:
            print(f"ERROR: Failed to launch app: {e}")

    def LaunchSearch(self, terms: List[str], timestamp: int):
        """GNOME Shell SearchProvider2 interface method"""

        print(f"DEBUG: LaunchSearch called with: {terms}")
        self._reset_idle_timer()
        
        try:
            subprocess.run(
                [
                    '/app/bin/devtoolbox',
                    '--search', ' '.join(terms)
                ],
                check=True,
            )
        except Exception as e:
            print(f"ERROR: Failed to launch search: {e}")

    def run(self):
        """Start the search provider D-Bus service"""

        print("DEBUG: Starting search provider D-Bus service...")

        try:
            # Get the session bus
            self._bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
            print("DEBUG: Connected to session bus")

            # Register the interface
            node_info = Gio.DBusNodeInfo.new_for_xml(self.interface_xml)
            interface_info = node_info.interfaces[0]
            print("DEBUG: Parsed interface XML")

            def handle_method_call(connection, sender, object_path, interface_name, method_name, parameters, invocation):
                print(f"DEBUG: Method called: {method_name}")
                try:
                    if method_name == "GetInitialResultSet":
                        terms = parameters.unpack()[0]
                        results = self.GetInitialResultSet(terms)
                        invocation.return_value(
                            GLib.Variant('(as)', (results,)))

                    elif method_name == "GetSubsearchResultSet":
                        previous_results, terms = parameters.unpack()
                        results = self.GetSubsearchResultSet(
                            previous_results, terms)
                        invocation.return_value(
                            GLib.Variant('(as)', (results,)))

                    elif method_name == "GetResultMetas":
                        identifiers = parameters.unpack()[0]
                        metas = self.GetResultMetas(identifiers)
                        invocation.return_value(
                            GLib.Variant('(aa{sv})', (metas,)))

                    elif method_name == "ActivateResult":
                        identifier, terms, timestamp = parameters.unpack()
                        self.ActivateResult(identifier, terms, timestamp)
                        invocation.return_value(None)

                    elif method_name == "LaunchSearch":
                        terms, timestamp = parameters.unpack()
                        self.LaunchSearch(terms, timestamp)
                        invocation.return_value(None)

                    else:
                        invocation.return_error_literal(
                            Gio.dbus_error_quark(),
                            Gio.DBusError.UNKNOWN_METHOD,
                            f"Unknown method: {method_name}"
                        )

                except Exception as e:
                    print(f"ERROR in {method_name}: {e}")
                    invocation.return_error_literal(
                        Gio.dbus_error_quark(),
                        Gio.DBusError.FAILED,
                        str(e)
                    )

            # Register the object
            self._registration_id = self._bus.register_object(
                "/me/iepure/devtoolbox/SearchProvider",
                interface_info,
                handle_method_call,
                None,  # get_property
                None   # set_property
            )

            print(f"DEBUG: Registered object with ID: {self._registration_id}")

            # Own the name
            name_id = Gio.bus_own_name(
                Gio.BusType.SESSION,
                "me.iepure.devtoolbox.SearchProvider",
                Gio.BusNameOwnerFlags.NONE,
                None,  # bus_acquired_closure
                None,  # name_acquired_closure
                None   # name_lost_closure
            )

            print(f"DEBUG: Name ownership ID: {name_id}")
            print("DEBUG: Search provider service started. Waiting for requests...")

            self._reset_idle_timer()

            # Run the main loop
            self._main_loop = GLib.MainLoop()
            self._main_loop.run()

        except Exception as e:
            print(f"ERROR: Failed to start search provider: {e}")
            return 1

        return 0
