/*
 * config_format.rs
 *
 * Copyright (C) 2022-2025 Alessandro Iepure
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even implied warranty of
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
            .property("title", metadata.title)
            .property("description", metadata.description)
            .build()
    }
}
