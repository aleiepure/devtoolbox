/*
 * lipsum.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::prelude::ComboRowExt;
use adw::subclass::prelude::*;
use gtk::{glib, glib::Properties, CompositeTemplate};

use crate::{core::widgets::TextArea, tools::lipsum::lorem};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/lipsum/lipsum.ui")]
    #[properties(wrapper_type = super::LipsumWidget)]
    pub struct LipsumWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        begin_with_lorem_switchrow: TemplateChild<adw::SwitchRow>,

        #[template_child]
        length_type_comborow: TemplateChild<adw::ComboRow>,

        #[template_child]
        length_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        output_area: TemplateChild<TextArea>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for LipsumWidget {
        const NAME: &'static str = "LipsumWidget";
        type Type = super::LipsumWidget;
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
    impl LipsumWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_active_begin_with_lorem_switchrow(&self) {
            self.update_output_area();
        }

        #[template_callback]
        fn on_signal_notify_selected_length_type_comborow(&self) {
            self.update_output_area();
        }

        #[template_callback]
        fn on_signal_notify_value_length_spinrow(&self) {
            self.update_output_area();
        }

        #[template_callback]
        fn on_signal_error_output_area(&self, error: &str) {
            self.output_area.set_error(true);
            self.output_area.set_error_label(error);
        }

        // Other methods
        fn update_output_area(&self) {
            let begin_with_lorem = self.begin_with_lorem_switchrow.is_active();
            let length_type = self.length_type_comborow.selected() as usize;
            let length_value = self.length_spinrow.value() as usize;

            let generated_text = match length_type {
                0 => lorem::generate_sentence(Some(length_value)),
                1 => lorem::generate_paragraph(Some(length_value)),
                2 => lorem::generate_paragraphs(Some(length_value)),
                _ => String::new(),
            };

            let final_text = if begin_with_lorem {
                let first_char = generated_text
                    .chars()
                    .nth(0)
                    .unwrap()
                    .to_lowercase()
                    .collect::<String>();
                let generated_text = first_char + &generated_text[1..];
                format!("Lorem ipsum dolor sit amet, {}", generated_text)
            } else {
                generated_text
            };

            self.output_area.set_error(false);
            self.output_area.set_text(final_text);
        }
    }

    impl ObjectImpl for LipsumWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.update_output_area();
        }
    }

    impl WidgetImpl for LipsumWidget {}
    impl BinImpl for LipsumWidget {}
}

glib::wrapper! {
    pub struct LipsumWidget(ObjectSubclass<imp::LipsumWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl LipsumWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
