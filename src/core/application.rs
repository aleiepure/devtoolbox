/* application.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use adw::prelude::*;
use adw::subclass::prelude::*;
use gtk::{gio, glib};

use crate::config::{APP_NAME, VERSION};
use crate::DevtoolboxWindow;

mod imp {
    use super::*;

    #[derive(Debug, Default)]
    pub struct DevtoolboxApplication {}

    #[glib::object_subclass]
    impl ObjectSubclass for DevtoolboxApplication {
        const NAME: &'static str = "DevtoolboxApplication";
        type Type = super::DevtoolboxApplication;
        type ParentType = adw::Application;
    }

    impl ObjectImpl for DevtoolboxApplication {
        fn constructed(&self) {
            self.parent_constructed();
            let obj = self.obj();
            obj.setup_gactions();
            obj.set_accels_for_action("app.quit", &["<control>q"]);
        }
    }

    impl ApplicationImpl for DevtoolboxApplication {
        fn startup(&self) {
            self.parent_startup();
            sourceview::init();
        }

        // We connect to the activate callback to create a window when the application
        // has been launched. Additionally, this callback notifies us when the user
        // tries to launch a "second instance" of the application. When they try
        // to do that, we'll just present any existing window.
        fn activate(&self) {
            let application = self.obj();
            // Get the current window or create one if necessary
            let window = application.active_window().unwrap_or_else(|| {
                let window = DevtoolboxWindow::new(&*application);
                window.upcast()
            });

            // Ask the window manager/compositor to present the window
            window.present();
        }
    }

    impl GtkApplicationImpl for DevtoolboxApplication {}
    impl AdwApplicationImpl for DevtoolboxApplication {}
}

glib::wrapper! {
    pub struct DevtoolboxApplication(ObjectSubclass<imp::DevtoolboxApplication>)
        @extends gio::Application, gtk::Application, adw::Application,
        @implements gio::ActionGroup, gio::ActionMap;
}

impl DevtoolboxApplication {
    pub fn new(application_id: &str, flags: &gio::ApplicationFlags) -> Self {
        glib::Object::builder()
            .property("application-id", application_id)
            .property("flags", flags)
            .property("resource-base-path", "/me/iepure/devtoolbox")
            .build()
    }

    fn setup_gactions(&self) {
        let quit_action = gio::ActionEntry::builder("quit")
            .activate(move |app: &Self, _, _| {
                // TODO: cleanup temporary files
                app.quit()
            })
            .build();

        let about_action = gio::ActionEntry::builder("about")
            .activate(move |app: &Self, _, _| app.show_about())
            .build();

        let show_tool_action = gio::ActionEntry::builder("show-tool")
            .parameter_type(Some(&str::static_variant_type()))
            .activate(move |app: &Self, _, parameter| {
                if let Some(tool_id) = parameter {
                    if let Some(window) = app.active_window() {
                        window
                            .downcast_ref::<DevtoolboxWindow>()
                            .unwrap()
                            .show_tool(&tool_id.get::<String>().unwrap_or_default());
                    }
                }
            })
            .build();

        let search_action = gio::ActionEntry::builder("search")
            .parameter_type(Some(&str::static_variant_type()))
            .activate(move |app: &Self, _, parameter| {
                if let Some(query) = parameter {
                    if let Some(window) = app.active_window() {
                        window
                            .downcast_ref::<DevtoolboxWindow>()
                            .unwrap()
                            .search_tools(&query.get::<String>().unwrap_or_default());
                    }
                }
            })
            .build();

        self.add_action_entries([quit_action, about_action, show_tool_action, search_action]);
    }

    fn show_about(&self) {
        let window = self.active_window().unwrap();
        let about_dialog =
            gtk::Builder::from_resource("/me/iepure/devtoolbox/core/ui/about-dialog.ui")
                .object::<adw::AboutDialog>("about_dialog")
                .unwrap();

        about_dialog.set_application_name(APP_NAME);
        about_dialog.set_application_icon("me.iepure.devtoolbox");
        about_dialog.set_version(VERSION);
        about_dialog.present(Some(&window));
    }
}
