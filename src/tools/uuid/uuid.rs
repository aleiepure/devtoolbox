/*
 * uuid.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::prelude::ComboRowExt;
use adw::subclass::prelude::*;
use gtk::{glib, CompositeTemplate};
use mac_address::get_mac_address;
use uuid::Uuid;

use crate::core::widgets::TextArea;

enum UUIDVersion {
    V1,
    V3,
    V4,
    V5,
    V6,
    V7,
}

impl UUIDVersion {
    fn from_index(index: u32) -> Option<Self> {
        match index {
            0 => Some(UUIDVersion::V1),
            1 => Some(UUIDVersion::V3),
            2 => Some(UUIDVersion::V4),
            3 => Some(UUIDVersion::V5),
            4 => Some(UUIDVersion::V6),
            5 => Some(UUIDVersion::V7),
            _ => None,
        }
    }
}

// ----------------------------------------------------------------------------

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/uuid/uuid.ui")]
    pub struct UuidWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        version_comborow: TemplateChild<adw::ComboRow>,

        #[template_child]
        length_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        output_area: TemplateChild<TextArea>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for UuidWidget {
        const NAME: &'static str = "UuidWidget";
        type Type = super::UuidWidget;
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
    impl UuidWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_selected_version_comborow(&self) {
            self.generate_uuid();
        }

        #[template_callback]
        fn on_signal_notify_value_length_spinrow(&self) {
            self.generate_uuid();
        }

        #[template_callback]
        fn on_signal_error_output_area(&self, error: &str) {
            self.output_area.set_error(true);
            self.output_area.set_error_label(error);
        }

        // Other methods
        fn generate_uuid(&self) {
            self.output_area.set_error(false);

            let version = UUIDVersion::from_index(self.version_comborow.selected())
                .unwrap_or(UUIDVersion::V4);
            let length = self.length_spinrow.value() as usize;

            let uuids = match version {
                UUIDVersion::V1 => (0..length)
                    .map(|_| Uuid::now_v1(&get_mac_address().unwrap().unwrap().bytes()).to_string())
                    .collect::<Vec<String>>(),
                UUIDVersion::V3 => (0..length)
                    .map(|_| {
                        Uuid::new_v3(&Uuid::NAMESPACE_DNS, self.random_string().as_bytes())
                            .to_string()
                    })
                    .collect(),
                UUIDVersion::V4 => (0..length).map(|_| Uuid::new_v4().to_string()).collect(),
                UUIDVersion::V5 => (0..length)
                    .map(|_| {
                        Uuid::new_v5(&Uuid::NAMESPACE_DNS, self.random_string().as_bytes())
                            .to_string()
                    })
                    .collect(),
                UUIDVersion::V6 => (0..length)
                    .map(|_| Uuid::now_v6(&get_mac_address().unwrap().unwrap().bytes()).to_string())
                    .collect(),
                UUIDVersion::V7 => (0..length).map(|_| Uuid::now_v7().to_string()).collect(),
            };

            let output = uuids
                .iter()
                .map(|u| u.to_string())
                .collect::<Vec<_>>()
                .join("\n");
            self.output_area.set_text(output);
        }

        fn random_string(&self) -> String {
            let random_str: String = (0..16)
                .map(|_| {
                    let idx = rand::random::<usize>() % 36;
                    char::from_digit(idx as u32, 36).unwrap()
                })
                .collect();
            random_str
        }
    }

    impl ObjectImpl for UuidWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.version_comborow.set_selected(2);

            self.generate_uuid();
        }
    }

    impl WidgetImpl for UuidWidget {}
    impl BinImpl for UuidWidget {}
}

glib::wrapper! {
    pub struct UuidWidget(ObjectSubclass<imp::UuidWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl UuidWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
