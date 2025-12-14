/* window.rs
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

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gio, glib, CompositeTemplate};

mod imp {
    use gtk::gio::Settings;

    use crate::config::APP_ID;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/Devtoolbox/core/ui/window.ui")]
    pub struct DevtoolboxWindow {
        // Template widgets
        #[template_child]
        pub overlay_split_view: TemplateChild<adw::OverlaySplitView>,

        #[template_child]
        pub toggle_sidebar_button: TemplateChild<gtk::ToggleButton>,

        #[template_child]
        pub menu_button: TemplateChild<gtk::MenuButton>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for DevtoolboxWindow {
        const NAME: &'static str = "DevtoolboxWindow";
        type Type = super::DevtoolboxWindow;
        type ParentType = adw::ApplicationWindow;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl DevtoolboxWindow {
        #[template_callback]
        fn on_signal_row_activated_favorite_listbox(&self, row: &gtk::ListBoxRow) {
            println!("Row activated: {:?}", row);
            // TODO: implement favorite tool activation
        }

        #[template_callback]
        fn on_signal_search_changed_search_entry(entry: &gtk::SearchEntry) {
            println!("Search changed: {:?}", entry);
            // TODO: implement tool search filtering
        }

        #[template_callback]
        fn on_signal_row_activated_sidebar_listbox(&self, row: &gtk::ListBoxRow) {
            println!("Sidebar row activated: {:?}", row);
            // TODO: implement sidebar tool activation
        }

        #[template_callback]
        fn on_signal_clicked_show_sidebar_button(button: &gtk::Button) {
            let window = button
                .ancestor(super::DevtoolboxWindow::static_type())
                .and_downcast::<super::DevtoolboxWindow>()
                .expect("Button should be inside DevtoolboxWindow");

            window.imp().overlay_split_view.set_show_sidebar(true);
        }
    }

    impl ObjectImpl for DevtoolboxWindow {
        fn constructed(&self) {
            self.parent_constructed();

            // TODO: remove 'devel' css class if not in debug mode
            // TODO: figure out why shortcut dialog is disabled

            // Bind settings
            let settings = Settings::new(APP_ID);
            settings
                .bind(
                    "window-width",
                    self.obj().upcast_ref::<gtk::Window>(),
                    "default-width",
                )
                .build();
            settings
                .bind(
                    "window-height",
                    self.obj().upcast_ref::<gtk::Window>(),
                    "default-height",
                )
                .build();
            settings
                .bind(
                    "window-maximized",
                    self.obj().upcast_ref::<gtk::Window>(),
                    "maximized",
                )
                .build();
            settings
                .bind("sidebar-open", &self.toggle_sidebar_button.get(), "active")
                .build();
            // TODO: restore last opened tool
            // settings.bind("last-tool", &self.content_stack, "visible-child-name").build();
        }
    }

    impl WidgetImpl for DevtoolboxWindow {}
    impl WindowImpl for DevtoolboxWindow {}
    impl ApplicationWindowImpl for DevtoolboxWindow {}
    impl AdwApplicationWindowImpl for DevtoolboxWindow {}
}

glib::wrapper! {
    pub struct DevtoolboxWindow(ObjectSubclass<imp::DevtoolboxWindow>)
        @extends gtk::Widget, gtk::Window, gtk::ApplicationWindow, adw::ApplicationWindow,
                 gtk::Native, gtk::Root, gtk::ShortcutManager,
        @implements gio::ActionGroup, gio::ActionMap, gtk::ConstraintTarget, gtk::Buildable, gtk::Accessible;
}

impl DevtoolboxWindow {
    pub fn new<P: IsA<gtk::Application>>(application: &P) -> Self {
        glib::Object::builder()
            .property("application", application)
            .build()
    }
}
