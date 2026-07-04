/* main.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

mod config;
mod core;
mod tools;

use core::application::DevtoolboxApplication;
use core::widgets::{ActionableEntryRow, ImageArea, TextArea};
use core::window::DevtoolboxWindow;

use config::{GETTEXT_PACKAGE, LOCALEDIR, PKGDATADIR};
use gettextrs::{bind_textdomain_codeset, bindtextdomain, textdomain};
use gtk::prelude::*;
use gtk::{gio, glib};

use crate::core::search_provider::SearchProviderApp;

fn main() -> glib::ExitCode {
    // -- Search Provider mode (headless) --
    if std::env::args().any(|arg| arg == "--search-provider") {
        return run_search_provider();
    }

    // -- GUI mode --
    // Set up gettext translations
    bindtextdomain(GETTEXT_PACKAGE, LOCALEDIR).expect("Unable to bind the text domain");
    bind_textdomain_codeset(GETTEXT_PACKAGE, "UTF-8")
        .expect("Unable to set the text domain encoding");
    textdomain(GETTEXT_PACKAGE).expect("Unable to switch to the text domain");

    // Load resources
    let resources = gio::Resource::load(PKGDATADIR.to_owned() + "/devtoolbox.gresource")
        .expect("Could not load resources");
    gio::resources_register(&resources);

    // Register custom widgets
    TextArea::ensure_type();
    ActionableEntryRow::ensure_type();
    ImageArea::ensure_type();

    let app = DevtoolboxApplication::new(
        "me.iepure.devtoolbox",
        &gio::ApplicationFlags::HANDLES_COMMAND_LINE,
    );

    app.run()
}

/// Run the search provider in headless mode
fn run_search_provider() -> glib::ExitCode {
    let resources = gio::Resource::load(PKGDATADIR.to_owned() + "/devtoolbox.gresource")
        .expect("Could not load resources");
    gio::resources_register(&resources);

    let app = SearchProviderApp::new();
    let _guard = app.hold();
    app.run()
}
