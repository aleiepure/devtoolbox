/*
 * html_enc.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gdk, glib, glib::Properties, CompositeTemplate};

use gettextrs::gettext;
use std::cell::RefCell;

use crate::core::widgets::TextArea;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/html_enc/html_enc.ui")]
    #[properties(wrapper_type = super::HtmlEncWidget)]
    pub struct HtmlEncWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        direction_toggle_group: TemplateChild<adw::ToggleGroup>,

        #[template_child]
        input_area: TemplateChild<TextArea>,

        #[template_child]
        output_area: TemplateChild<TextArea>,

        // Properties
        #[property(set, get, type = bool, default = false)]
        dragging: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for HtmlEncWidget {
        const NAME: &'static str = "HtmlEncWidget";
        type Type = super::HtmlEncWidget;
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
    impl HtmlEncWidget {
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
        fn on_signal_cleared_input_area(&self) {
            self.output_area.clear();
            self.input_area.set_error(false);
            self.output_area.set_error(false);
        }

        #[template_callback]
        fn on_signal_error_input_area(&self, error_message: String) {
            self.input_area.set_error(true);
            self.input_area.set_error_label(error_message);
        }

        #[template_callback]
        fn on_signal_error_output_area(&self, error_message: String) {
            self.output_area.set_error(true);
            self.output_area.set_error_label(error_message);
        }

        // Other methods
        fn encode(&self) {
            let input_text = self.input_area.text();
            let encoded_text = htmlescape::encode_minimal(&input_text);
            self.output_area.set_text(encoded_text);
            self.input_area.set_error(false);
        }

        fn decode(&self) {
            let input_text = self.input_area.text();
            match htmlescape::decode_html(&input_text) {
                Ok(decoded_text) => {
                    self.output_area.set_text(decoded_text);
                    self.input_area.set_error(false);
                }
                Err(_err) => {
                    self.input_area.set_error(true);
                    self.input_area
                        .set_error_label(gettext("Invalid input. Check the syntax"));
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
    impl ObjectImpl for HtmlEncWidget {
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

    impl WidgetImpl for HtmlEncWidget {}
    impl BinImpl for HtmlEncWidget {}
}

glib::wrapper! {
    pub struct HtmlEncWidget(ObjectSubclass<imp::HtmlEncWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl HtmlEncWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
