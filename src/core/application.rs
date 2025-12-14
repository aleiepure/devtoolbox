/* application.rs
 *
 * Copyright (C) 2022-2025 Alessandro Iepure
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use adw::prelude::*;
use adw::subclass::prelude::*;
use gettextrs::gettext;
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
            .property("resource-base-path", "/me/iepure/Devtoolbox")
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
        self.add_action_entries([quit_action, about_action]);
    }

    fn show_about(&self) {
        let window = self.active_window().unwrap();
        let about_dialog =
            gtk::Builder::from_resource("/me/iepure/Devtoolbox/core/ui/about-dialog.ui")
                .object::<adw::AboutDialog>("about_dialog")
                .unwrap();

        about_dialog.set_application_name(APP_NAME);
        about_dialog.set_application_icon("me.iepure.Devtoolbox");
        about_dialog.set_version(VERSION);
        about_dialog.add_credit_section(
            Some(&gettext("Contributors")),
            &[
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
            ],
        );

        about_dialog.present(Some(&window));
    }
}
