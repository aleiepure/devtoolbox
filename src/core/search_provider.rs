/*
 * search_provider.rs
 *
 * Copyright (C) 2026 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use gtk::{
    gio::{self, prelude::*, subclass::prelude::*, DBusError},
    glib,
};

use std::{cell::RefCell, collections::HashMap, time::Instant};

// Constants
const IDLE_TIMEOUT_SECS: u32 = 10;
const CACHE_DURATION_SECS: u64 = 300;

const SEARCH_PROVIDER_INTERFACE: &str = "org.gnome.Shell.SearchProvider2";
const SEARCH_PROVIDER_OBJECT_PATH: &str = "/me/iepure/devtoolbox/SearchProvider";

const SEARCH_PROVIDER_XML: &str =
    include_str!("../../data/me.iepure.devtoolbox.SearchProvider.xml");

// Variant types for D-Bus method arguments
#[derive(Debug, glib::Variant)]
struct GetInitialResultSetCall {
    terms: Vec<String>,
}

#[derive(Debug, glib::Variant)]
struct GetSubsearchResultSetCall {
    previous_results: Vec<String>,
    terms: Vec<String>,
}

#[derive(Debug, glib::Variant)]
struct GetResultMetasCall {
    identifiers: Vec<String>,
}

#[derive(Debug, glib::Variant)]
struct ActivateResultCall {
    identifier: String,
    terms: Vec<String>,
    timestamp: u32,
}

#[derive(Debug, glib::Variant)]
struct LaunchSearchCall {
    terms: Vec<String>,
    timestamp: u32,
}

// Method call enum
#[derive(Debug)]
enum SearchProviderMethod {
    GetInitialResultSet(GetInitialResultSetCall),
    GetSubsearchResultSet(GetSubsearchResultSetCall),
    GetResultMetas(GetResultMetasCall),
    ActivateResult(ActivateResultCall),
    LaunchSearch(LaunchSearchCall),
}

impl DBusMethodCall for SearchProviderMethod {
    fn parse_call(
        _obj_path: &str,
        _interface: Option<&str>,
        method: &str,
        params: glib::Variant,
    ) -> Result<Self, glib::Error> {
        match method {
            "GetInitialResultSet" => params
                .get::<GetInitialResultSetCall>()
                .map(Self::GetInitialResultSet)
                .ok_or_else(|| glib::Error::new(DBusError::InvalidArgs, "Invalid parameters")),

            "GetSubsearchResultSet" => params
                .get::<GetSubsearchResultSetCall>()
                .map(Self::GetSubsearchResultSet)
                .ok_or_else(|| glib::Error::new(DBusError::InvalidArgs, "Invalid parameters")),

            "GetResultMetas" => params
                .get::<GetResultMetasCall>()
                .map(Self::GetResultMetas)
                .ok_or_else(|| glib::Error::new(DBusError::InvalidArgs, "Invalid parameters")),

            "ActivateResult" => params
                .get::<ActivateResultCall>()
                .map(Self::ActivateResult)
                .ok_or_else(|| glib::Error::new(DBusError::InvalidArgs, "Invalid parameters")),

            "LaunchSearch" => params
                .get::<LaunchSearchCall>()
                .map(Self::LaunchSearch)
                .ok_or_else(|| glib::Error::new(DBusError::InvalidArgs, "Invalid parameters")),

            _ => Err(glib::Error::new(
                DBusError::UnknownMethod,
                &format!("Unknown method: {}", method),
            )),
        }
    }
}

// Internal state
mod imp {

    use crate::tools;

    use super::*;

    pub struct SearchProviderApp {
        registration_id: RefCell<Option<gio::RegistrationId>>,
        idle_timeout_id: RefCell<Option<glib::SourceId>>,
        search_cache: RefCell<HashMap<String, (Vec<String>, Instant)>>,
    }

    impl Default for SearchProviderApp {
        fn default() -> Self {
            Self {
                registration_id: RefCell::new(None),
                idle_timeout_id: RefCell::new(None),
                search_cache: RefCell::new(HashMap::new()),
            }
        }
    }

    #[glib::object_subclass]
    impl ObjectSubclass for SearchProviderApp {
        const NAME: &'static str = "SearchProviderApp";
        type Type = super::SearchProviderApp;
        type ParentType = gio::Application;
    }

    impl ObjectImpl for SearchProviderApp {
        fn constructed(&self) {
            self.parent_constructed();
        }
    }

    impl ApplicationImpl for SearchProviderApp {
        fn dbus_register(
            &self,
            connection: &gio::DBusConnection,
            object_path: &str,
        ) -> Result<(), glib::Error> {
            self.parent_dbus_register(connection, object_path)?;

            // Parse DBus interface
            let node_info = gio::DBusNodeInfo::for_xml(SEARCH_PROVIDER_XML).map_err(|e| {
                glib::Error::new(DBusError::Failed, &format!("XML parse error: {e}"))
            })?;
            let interface = node_info
                .lookup_interface(SEARCH_PROVIDER_INTERFACE)
                .ok_or_else(|| {
                    glib::Error::new(
                        DBusError::Failed,
                        &format!("Interface {SEARCH_PROVIDER_INTERFACE} not found in XML"),
                    )
                })?;

            let app_down = self.obj().downgrade();

            let id = connection
                .register_object(SEARCH_PROVIDER_OBJECT_PATH, &interface)
                .typed_method_call::<SearchProviderMethod>()
                .invoke_and_return_future_local(move |_connection, _sender, call| {
                    let app = app_down.clone();
                    async move {
                        // Guard against the app being dropped
                        let Some(app) = app.upgrade() else {
                            return Ok(None);
                        };

                        // Reset idle timeout
                        app.imp().reset_idle_timer();

                        match call {
                            SearchProviderMethod::GetInitialResultSet(params) => {
                                let results = app.imp().search_with_cache(&params.terms);
                                Ok(Some((results,).to_variant()))
                            }
                            SearchProviderMethod::GetSubsearchResultSet(params) => {
                                let results = app.imp().search_with_cache(&params.terms);
                                Ok(Some((results,).to_variant()))
                            }
                            SearchProviderMethod::GetResultMetas(params) => {
                                let metas = app.imp().build_result_metas(&params.identifiers);
                                Ok(Some(metas))
                            }
                            SearchProviderMethod::ActivateResult(params) => {
                                launch_app("--tool", &params.identifier);
                                Ok(None)
                            }
                            SearchProviderMethod::LaunchSearch(params) => {
                                launch_app("--search", &params.terms.join(" "));
                                Ok(None)
                            }
                        }
                    }
                })
                .build()?;

            self.registration_id.replace(Some(id));
            Ok(())
        }

        fn dbus_unregister(&self, connection: &gio::DBusConnection, object_path: &str) {
            self.parent_dbus_unregister(connection, object_path);
            if let Some(id) = self.registration_id.take() {
                if connection.unregister_object(id).is_err() {
                    eprintln!("Failed to unregister D-Bus object at {}", object_path);
                }
            }
        }
    }

    impl SearchProviderApp {
        fn reset_idle_timer(&self) {
            // Clear existing timer
            if let Some(id) = self.idle_timeout_id.take() {
                id.remove();
            }

            let app = self.obj().downgrade();
            let id = glib::timeout_add_seconds_local(IDLE_TIMEOUT_SECS, move || {
                if let Some(app) = app.upgrade() {
                    app.quit();
                }
                glib::ControlFlow::Break
            });

            self.idle_timeout_id.replace(Some(id));
        }

        fn search_with_cache(&self, terms: &[String]) -> Vec<String> {
            let cache_key = terms.join("|");
            let now = Instant::now();

            // Check cache
            {
                let cache = self.search_cache.borrow();
                if let Some((results, timestamp)) = cache.get(&cache_key) {
                    if now.duration_since(*timestamp).as_secs() < CACHE_DURATION_SECS {
                        return results.clone();
                    }
                }
            }

            // Do the search
            let search_terms: Vec<&str> = terms.iter().map(|s| s.as_str()).collect();
            let results: Vec<String> = tools::search_tools(&search_terms)
                .into_iter()
                .map(|tool| tool.id.to_string())
                .collect();

            // Cache result
            self.search_cache
                .borrow_mut()
                .insert(cache_key, (results.clone(), now));

            // Delete stale entries
            self.search_cache.borrow_mut().retain(|_, (_, timestamp)| {
                now.duration_since(*timestamp).as_secs() < CACHE_DURATION_SECS
            });

            results
        }

        fn build_result_metas(&self, identifiers: &[String]) -> glib::Variant {
            let mut dicts: Vec<glib::Variant> = Vec::new();

            for tool_id in identifiers {
                let Some(meta) = tools::ALL_TOOLS.iter().find(|tool| tool.id == tool_id) else {
                    continue;
                };

                let dict = glib::VariantDict::new(None);
                dict.insert("id", &meta.id);
                dict.insert("name", &meta.title);
                dict.insert("description", &meta.description);

                // todo: figure out how to add icons to the search provider results

                dicts.push(dict.end());
            }

            let child_type = glib::VariantTy::new("a{sv}").expect("Built-in type a{sv}");
            glib::Variant::array_from_iter_with_type(&child_type, &dicts)
        }
    }
}

// Public wrapper
glib::wrapper! {
    pub struct SearchProviderApp(ObjectSubclass<imp::SearchProviderApp>)
        @extends gio::Application,
        @implements gio::ActionGroup, gio::ActionMap;
}

impl SearchProviderApp {
    pub fn new() -> Self {
        glib::Object::builder()
            .property("application-id", "me.iepure.devtoolbox.SearchProvider")
            .property("flags", gio::ApplicationFlags::HANDLES_COMMAND_LINE)
            .build()
    }
}

impl Default for SearchProviderApp {
    fn default() -> Self {
        Self::new()
    }
}

fn launch_app(flag: &str, value: &str) {
    let bin = std::env::args()
        .next()
        .unwrap_or_else(|| "devtoolbox".into());
    std::process::Command::new(&bin)
        .args([flag, value])
        .spawn()
        .expect("Application failed to start");
}
