/*
 * timestamp.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

use crate::tools::ToolMetadata;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/timestamp/timestamp.ui")]
    #[properties(wrapper_type = super::TimestampWidget)]
    pub struct TimestampWidget {
        // Template widgets

        // Properties
        #[property(set, get, type = String)]
        tool_id: RefCell<String>,

        #[property(set, get, type = String)]
        title: RefCell<String>,

        #[property(set, get, type = String)]
        description: RefCell<String>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for TimestampWidget {
        const NAME: &'static str = "TimestampWidget";
        type Type = super::TimestampWidget;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            // klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    // #[gtk::template_callbacks]
    // impl ToolTitle {
    //     #[template_callback]
    //     fn function() {}
    // }

    #[glib::derived_properties]
    impl ObjectImpl for TimestampWidget {
        fn constructed(&self) {
            self.parent_constructed();
        }
    }

    impl WidgetImpl for TimestampWidget {}
    impl BinImpl for TimestampWidget {}
}

glib::wrapper! {
    pub struct TimestampWidget(ObjectSubclass<imp::TimestampWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

impl TimestampWidget {
    pub fn new(metadata: &ToolMetadata) -> Self {
        glib::Object::builder()
            .property("tool-id", metadata.id)
            .property("title", metadata.title.clone())
            .property("description", metadata.description.clone())
            .build()
    }
}
