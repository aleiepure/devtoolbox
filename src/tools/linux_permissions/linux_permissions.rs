/*
 * linux_permissions.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, CompositeTemplate};

use std::cell::RefCell;

mod imp {
    use crate::tools::linux_permissions::conversion;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/linux_permissions/linux_permissions.ui")]
    pub struct LinuxPermissionsWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        read_owner_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        read_group_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        read_others_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        write_owner_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        write_group_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        write_others_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        execute_owner_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        execute_group_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        execute_others_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        set_uid_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        set_gid_checkbutton: TemplateChild<gtk::CheckButton>,
        #[template_child]
        sticky_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        numeric_entryrow: TemplateChild<adw::EntryRow>,
        #[template_child]
        symbolic_entryrow: TemplateChild<adw::EntryRow>,

        // Other fields
        /// Flag to prevent recursive updates
        updating: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for LinuxPermissionsWidget {
        const NAME: &'static str = "LinuxPermissionsWidget";
        type Type = super::LinuxPermissionsWidget;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl LinuxPermissionsWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_toggled_read_owner_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_read_group_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_read_others_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_write_owner_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_write_group_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_write_others_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_execute_owner_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_execute_group_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_execute_others_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_set_uid_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_set_gid_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_toggled_sticky_checkbutton(&self) {
            if *self.updating.borrow() {
                return;
            }
            self.update_from_checkboxes();
        }

        #[template_callback]
        fn on_signal_changed_numeric_entryrow(&self) {
            if *self.updating.borrow() {
                return;
            }

            let text = self.numeric_entryrow.text();

            // Try parsing as octal number to catch invalid inputs
            match u16::from_str_radix(text.trim(), 8) {
                Ok(mode) => {
                    if mode <= 0o7777 {
                        // Valid
                        self.numeric_entryrow.remove_css_class("error");
                        self.update_from_numeric(mode);
                    } else {
                        // Out of range
                        self.numeric_entryrow.add_css_class("error");
                        self.uncheck_all_checkbuttons();
                    }
                }
                Err(_) => {
                    // Invalid input
                    self.numeric_entryrow.add_css_class("error");
                    self.uncheck_all_checkbuttons();
                }
            }
        }

        #[template_callback]
        fn on_signal_changed_symbolic_entryrow(&self) {
            if *self.updating.borrow() {
                return;
            }

            let text = self.symbolic_entryrow.text();

            match conversion::parse_from_symbolic(text.trim()) {
                Some(mode) => {
                    // Valid
                    self.symbolic_entryrow.remove_css_class("error");
                    self.update_from_numeric(mode);
                }
                None => {
                    // Invalid input
                    self.symbolic_entryrow.add_css_class("error");
                    self.uncheck_all_checkbuttons();
                }
            }
        }

        // Other methods
        fn update_from_checkboxes(&self) {
            let permissions = [
                self.read_owner_checkbutton.is_active(),
                self.write_owner_checkbutton.is_active(),
                self.execute_owner_checkbutton.is_active(),
                self.read_group_checkbutton.is_active(),
                self.write_group_checkbutton.is_active(),
                self.execute_group_checkbutton.is_active(),
                self.read_others_checkbutton.is_active(),
                self.write_others_checkbutton.is_active(),
                self.execute_others_checkbutton.is_active(),
            ];

            let special = [
                self.set_uid_checkbutton.is_active(),
                self.set_gid_checkbutton.is_active(),
                self.sticky_checkbutton.is_active(),
            ];

            let mode = conversion::parse_from_boolean_arrays(&permissions, &special);

            *self.updating.borrow_mut() = true;
            self.numeric_entryrow.set_text(&format!("{:04o}", mode));
            self.symbolic_entryrow
                .set_text(&conversion::numeric_to_symbolic(mode));
            self.numeric_entryrow.set_position(-1);
            self.symbolic_entryrow.set_position(-1);

            self.numeric_entryrow.remove_css_class("error");
            self.symbolic_entryrow.remove_css_class("error");

            *self.updating.borrow_mut() = false;
        }

        fn update_from_numeric(&self, mode: u16) {
            let (permissions, special) = conversion::to_boolean_array(mode);

            *self.updating.borrow_mut() = true;

            self.read_owner_checkbutton.set_active(permissions[0]);
            self.write_owner_checkbutton.set_active(permissions[1]);
            self.execute_owner_checkbutton.set_active(permissions[2]);

            self.read_group_checkbutton.set_active(permissions[3]);
            self.write_group_checkbutton.set_active(permissions[4]);
            self.execute_group_checkbutton.set_active(permissions[5]);

            self.read_others_checkbutton.set_active(permissions[6]);
            self.write_others_checkbutton.set_active(permissions[7]);
            self.execute_others_checkbutton.set_active(permissions[8]);

            self.set_uid_checkbutton.set_active(special[0]);
            self.set_gid_checkbutton.set_active(special[1]);
            self.sticky_checkbutton.set_active(special[2]);

            self.numeric_entryrow.set_text(&format!("{:04o}", mode));
            self.symbolic_entryrow
                .set_text(&conversion::numeric_to_symbolic(mode));
            self.numeric_entryrow.set_position(-1);
            self.symbolic_entryrow.set_position(-1);

            self.numeric_entryrow.remove_css_class("error");
            self.symbolic_entryrow.remove_css_class("error");

            *self.updating.borrow_mut() = false;
        }

        fn uncheck_all_checkbuttons(&self) {
            *self.updating.borrow_mut() = true;
            self.read_owner_checkbutton.set_active(false);
            self.write_owner_checkbutton.set_active(false);
            self.execute_owner_checkbutton.set_active(false);

            self.read_group_checkbutton.set_active(false);
            self.write_group_checkbutton.set_active(false);
            self.execute_group_checkbutton.set_active(false);

            self.read_others_checkbutton.set_active(false);
            self.write_others_checkbutton.set_active(false);
            self.execute_others_checkbutton.set_active(false);

            self.set_uid_checkbutton.set_active(false);
            self.set_gid_checkbutton.set_active(false);
            self.sticky_checkbutton.set_active(false);
            *self.updating.borrow_mut() = false;
        }
    }

    impl ObjectImpl for LinuxPermissionsWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.update_from_checkboxes();
        }
    }

    impl WidgetImpl for LinuxPermissionsWidget {}
    impl BinImpl for LinuxPermissionsWidget {}
}

glib::wrapper! {
    pub struct LinuxPermissionsWidget(ObjectSubclass<imp::LinuxPermissionsWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl LinuxPermissionsWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
