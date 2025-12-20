/*
 * tool_title.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gio::Settings, glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

mod imp {

    use crate::config::APP_ID;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/core/widgets/tool_title/tool_title.ui")]
    #[properties(wrapper_type = super::ToolTitle)]
    pub struct ToolTitle {
        // Template widgets
        #[template_child]
        star_button: TemplateChild<gtk::Button>,

        // Properties
        #[property(set, get, type = String)]
        title: RefCell<String>,

        #[property(set, get, type = String)]
        description: RefCell<String>,

        #[property(set, get, type = String)]
        tool_id: RefCell<String>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for ToolTitle {
        const NAME: &'static str = "ToolTitle";
        type Type = super::ToolTitle;
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
    impl ToolTitle {
        #[template_callback]
        fn on_signal_clicked_star_button(&self, _button: &gtk::Button) {
            let settings = Settings::new(APP_ID);
            let mut favorites = settings.strv("favorite-tools");

            if favorites.contains(self.tool_id.borrow().as_str()) {
                self.star_button
                    .set_icon_name("star-outline-rounded-symbolic");

                let index = favorites
                    .iter()
                    .position(|id| id == self.tool_id.borrow().as_str())
                    .unwrap();
                favorites.remove(index);
                settings.set_strv("favorite-tools", &favorites).unwrap();
            } else {
                self.star_button
                    .set_icon_name("star-filled-rounded-symbolic");
                favorites.push(self.tool_id.borrow().as_str().into());
                settings.set_strv("favorite-tools", &favorites).unwrap();
            }
        }

        #[template_callback]
        fn start_button_icon_closure(&self, tool_id: &str) -> String {
            let settings = Settings::new(APP_ID);
            if settings
                .strv("favorite-tools")
                .contains(&tool_id.to_string())
            {
                "star-filled-rounded-symbolic".to_string()
            } else {
                "star-outline-rounded-symbolic".to_string()
            }

            // TODO: implement favorites menu refresh
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for ToolTitle {
        fn constructed(&self) {
            self.parent_constructed();
        }
    }

    impl WidgetImpl for ToolTitle {}
    impl BinImpl for ToolTitle {}
}

glib::wrapper! {
    pub struct ToolTitle(ObjectSubclass<imp::ToolTitle>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

impl ToolTitle {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
