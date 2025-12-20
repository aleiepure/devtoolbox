/*
 * config_format.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gdk, glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

use crate::tools::ToolMetadata;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/config_format/config_format.ui")]
    #[properties(wrapper_type = super::ConfigFormatWidget)]
    pub struct ConfigFormatWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        input_format_toggle_group: TemplateChild<adw::ToggleGroup>,

        #[template_child]
        output_format_toggle_group: TemplateChild<adw::ToggleGroup>,

        // Properties
        #[property(set, get, type = String)]
        tool_id: RefCell<String>,

        #[property(set, get, type = String)]
        title: RefCell<String>,

        #[property(set, get, type = String)]
        description: RefCell<String>,

        #[property(set, get, type = bool, default = false)]
        dragging: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for ConfigFormatWidget {
        const NAME: &'static str = "ConfigFormatWidget";
        type Type = super::ConfigFormatWidget;
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
    impl ConfigFormatWidget {
        #[template_callback]
        fn is_format_enabled_closure(&self, active: u32, index: i32) -> bool {
            active != index.try_into().unwrap()
        }

        #[template_callback]
        fn on_signal_notify_active_input_format_toggle_group(&self) {}

        #[template_callback]
        fn on_signal_notify_active_output_format_toggle_group(&self) {}

        #[template_callback]
        fn on_signal_input_area_action_button_clicked(&self) {
            println!("Input area action button clicked");
        }

        #[template_callback]
        fn on_signal_input_area_error(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for ConfigFormatWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Initialize toggle groups
            let input_group = self.input_format_toggle_group.clone();
            let output_group = self.output_format_toggle_group.clone();
            glib::idle_add_local(move || {
                input_group.set_active(0);
                output_group.set_active(1);
                glib::ControlFlow::Break
            });

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

    impl WidgetImpl for ConfigFormatWidget {}
    impl BinImpl for ConfigFormatWidget {}
}

glib::wrapper! {
    pub struct ConfigFormatWidget(ObjectSubclass<imp::ConfigFormatWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

impl ConfigFormatWidget {
    pub fn new(metadata: &ToolMetadata) -> Self {
        glib::Object::builder()
            .property("tool-id", metadata.id)
            .property("title", metadata.title)
            .property("description", metadata.description)
            .build()
    }
}
