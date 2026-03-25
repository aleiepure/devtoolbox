/*
 * url_enc.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::{glib, CompositeTemplate};
use pct_str::{PctString, UriReserved};

use crate::core::widgets::TextArea;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/url_enc/url_enc.ui")]
    pub struct UrlEncWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        direction_toggle_group: TemplateChild<adw::ToggleGroup>,

        #[template_child]
        input_area: TemplateChild<TextArea>,

        #[template_child]
        output_area: TemplateChild<TextArea>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for UrlEncWidget {
        const NAME: &'static str = "UrlEncWidget";
        type Type = super::UrlEncWidget;
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
    impl UrlEncWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_active_direction_toggle_group(&self) {
            self.do_conversion();
        }

        #[template_callback]
        fn on_signal_changed_input_area(&self) {
            self.do_conversion();
        }

        #[template_callback]
        fn on_signal_error_input_area(&self, error_message: String) {
            self.input_area.set_error(true);
            self.input_area.set_error_label(error_message);
        }

        #[template_callback]
        fn on_signal_cleared_input_area(&self) {
            self.output_area.clear();
            self.input_area.set_error(false);
            self.output_area.set_error(false);
        }

        #[template_callback]
        fn on_signal_error_output_area(&self, error_message: String) {
            self.output_area.set_error(true);
            self.output_area.set_error_label(error_message);
        }

        // Other methods
        fn encode(&self) {
            let pct_string = PctString::encode(self.input_area.text().chars(), UriReserved::Any);
            self.output_area.set_text(pct_string.to_string());
            self.input_area.set_error(false);
            self.output_area.set_error(false);
        }

        fn decode(&self) {
            let decoded_string = PctString::new(self.input_area.text());
            match decoded_string {
                Ok(pct_str) => self.output_area.set_text(pct_str.decode()),
                Err(_) => {}
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

    impl ObjectImpl for UrlEncWidget {}
    impl WidgetImpl for UrlEncWidget {}
    impl BinImpl for UrlEncWidget {}
}

glib::wrapper! {
    pub struct UrlEncWidget(ObjectSubclass<imp::UrlEncWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl UrlEncWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
