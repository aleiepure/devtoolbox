/*
 * base64.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gdk, glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

use crate::core::widgets::TextArea;

use base64::engine::general_purpose::URL_SAFE;
use base64::prelude::*;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/devtoolbox/tools/base64/base64.ui")]
    #[properties(wrapper_type = super::Base64Widget)]
    pub struct Base64Widget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        direction_toggle_group: TemplateChild<adw::ToggleGroup>,

        #[template_child]
        url_safe_switchrow: TemplateChild<adw::SwitchRow>,

        #[template_child]
        input_area: TemplateChild<TextArea>,

        #[template_child]
        output_area: TemplateChild<TextArea>,

        // Properties
        #[property(set, get, type = bool, default = false)]
        dragging: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for Base64Widget {
        const NAME: &'static str = "Base64Widget";
        type Type = super::Base64Widget;
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
    impl Base64Widget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_active_direction_toggle_group(&self) {
            self.do_conversion();
        }

        #[template_callback]
        fn on_signal_notify_active_url_safe_switchrow(&self) {
            self.do_conversion();
        }

        #[template_callback]
        fn on_signal_changed_input_area(&self) {
            self.do_conversion();
        }

        #[template_callback]
        fn on_signal_cleared_input_area(&self) {
            self.output_area.clear();
            self.toast_overlay.dismiss_all();
        }

        #[template_callback]
        fn on_signal_error_input_area(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }

        #[template_callback]
        fn on_signal_error_output_area(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }

        // Other methods
        fn encode(&self) {
            if self.url_safe_switchrow.is_active() {
                // URL Safe Base64 encoding
                let input_text = self.input_area.text();
                let encoded = URL_SAFE.encode(input_text);
                self.output_area.set_text(encoded);
            } else {
                // Standard Base64 encoding
                let input_text = self.input_area.text();
                let encoded = BASE64_STANDARD.encode(input_text);
                self.output_area.set_text(encoded);
            }
        }

        fn decode(&self) {
            if self.url_safe_switchrow.is_active() {
                // URL Safe Base64 decoding
                let input_text = self.input_area.text();
                match URL_SAFE.decode(input_text) {
                    Ok(decoded_bytes) => {
                        let decoded_text = String::from_utf8_lossy(&decoded_bytes).to_string();
                        self.output_area.set_text(decoded_text);
                        self.input_area.set_error(false);
                    }
                    Err(_err) => {
                        self.input_area.set_error(true);
                        self.input_area
                            .set_error_label("Invalid URL Safe Base64 input");
                    }
                }
            } else {
                // Standard Base64 decoding
                let input_text = self.input_area.text();
                match BASE64_STANDARD.decode(input_text) {
                    Ok(decoded_bytes) => {
                        let decoded_text = String::from_utf8_lossy(&decoded_bytes).to_string();
                        self.output_area.set_text(decoded_text);
                        self.input_area.set_error(false);
                    }
                    Err(_err) => {
                        self.input_area.set_error(true);
                        self.input_area.set_error_label("Invalid Base64 input");
                    }
                }
            }
        }

        fn do_conversion(&self) {
            if self.direction_toggle_group.active() == 0 {
                self.encode();
            } else {
                self.decode();
            }
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for Base64Widget {
        fn constructed(&self) {
            self.parent_constructed();

            // Drag and drop
            let drop_target =
                gtk::DropTarget::new(gdk::FileList::static_type(), gdk::DragAction::COPY);

            let obj = self.obj().clone();
            drop_target.connect_enter(move |_, _, _| {
                obj.set_dragging(true);
                gdk::DragAction::COPY
            });

            let obj = self.obj().clone();
            drop_target.connect_leave(move |_| {
                obj.set_dragging(false);
            });

            self.obj().add_controller(drop_target);
        }
    }

    impl WidgetImpl for Base64Widget {}
    impl BinImpl for Base64Widget {}
}

glib::wrapper! {
    pub struct Base64Widget(ObjectSubclass<imp::Base64Widget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl Base64Widget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
