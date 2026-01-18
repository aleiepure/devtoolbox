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

use crate::core::widgets::text_area::TextArea;
use crate::tools::config_format::convertion::{
    json_to_toml, json_to_yaml, toml_to_json, toml_to_yaml, validate_json, validate_toml,
    validate_yaml, yaml_to_json, yaml_to_toml, ConfigFormat,
};

mod imp {
    use std::cell::Cell;

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

        #[template_child]
        input_area: TemplateChild<TextArea>,

        #[template_child]
        output_area: TemplateChild<TextArea>,

        // Properties
        #[property(set, get, type = String)]
        tool_id: RefCell<String>,

        #[property(set, get, type = String)]
        title: RefCell<String>,

        #[property(set, get, type = String)]
        description: RefCell<String>,

        #[property(set, get, type = bool, default = false)]
        dragging: RefCell<bool>,

        // MARK: Other fields
        initialized: Cell<bool>,
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
            active != index as u32
        }

        #[template_callback]
        fn on_signal_notify_active_input_format_toggle_group(&self) {
            if self.initialized.get() {
                self.input_area.set_language(
                    ConfigFormat::try_from(self.input_format_toggle_group.active())
                        .unwrap()
                        .to_str(),
                );
                self.do_conversion();
            }
        }

        #[template_callback]
        fn on_signal_notify_active_output_format_toggle_group(&self) {
            if self.initialized.get() {
                self.output_area.set_language(
                    ConfigFormat::try_from(self.output_format_toggle_group.active())
                        .unwrap()
                        .to_str(),
                );
                self.do_conversion();
            }
        }

        #[template_callback]
        fn on_signal_input_area_changed(&self) {
            if self.initialized.get() {
                self.do_conversion();
            }
        }

        #[template_callback]
        fn on_signal_input_area_cleared(&self) {
            if self.initialized.get() {
                self.output_area.clear();
            }
            self.toast_overlay.dismiss_all();
        }

        #[template_callback]
        fn on_signal_input_area_error(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }

        #[template_callback]
        fn on_signal_output_area_error(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }

        fn do_conversion(&self) {
            if !self.initialized.get() {
                return;
            }

            let input_text = self.input_area.text();

            if input_text.is_empty() {
                return;
            }

            let input_index = self.input_format_toggle_group.active();
            let output_index = self.output_format_toggle_group.active();
            let (Ok(input_format), Ok(output_format)) = (
                ConfigFormat::try_from(input_index),
                ConfigFormat::try_from(output_index),
            ) else {
                return;
            };

            // Validate input format
            match input_format {
                ConfigFormat::Json => {
                    if let Err(e) = validate_json(&input_text) {
                        self.input_area.set_error(true);
                        self.input_area
                            .set_error_label(format!("Invalid JSON: {}", e));
                        return;
                    } else {
                        self.input_area.set_error(false);
                    }
                }
                ConfigFormat::Yaml => {
                    if let Err(e) = validate_yaml(&input_text) {
                        self.input_area.set_error(true);
                        self.input_area
                            .set_error_label(format!("Invalid YAML: {}", e));
                        return;
                    } else {
                        self.input_area.set_error(false);
                    }
                }
                ConfigFormat::Toml => {
                    if let Err(e) = validate_toml(&input_text) {
                        self.input_area.set_error(true);
                        self.input_area
                            .set_error_label(format!("Invalid TOML: {}", e));
                        return;
                    } else {
                        self.input_area.set_error(false);
                    }
                }
            }

            // Perform conversion
            match (input_format, output_format) {
                (ConfigFormat::Json, ConfigFormat::Yaml) => match json_to_yaml(&input_text) {
                    Ok(yaml_string) => {
                        self.output_area.set_text(yaml_string);
                        self.output_area.set_error(false);
                    }
                    Err(e) => {
                        self.output_area.set_error(true);
                        self.output_area
                            .set_error_label(format!("Conversion error: {}", e));
                    }
                },
                (ConfigFormat::Json, ConfigFormat::Toml) => match json_to_toml(&input_text) {
                    Ok(toml_string) => {
                        self.output_area.set_text(toml_string);
                        self.output_area.set_error(false);
                    }
                    Err(e) => {
                        self.output_area.set_error(true);
                        self.output_area
                            .set_error_label(format!("Conversion error: {}", e));
                    }
                },
                (ConfigFormat::Yaml, ConfigFormat::Json) => match yaml_to_json(&input_text) {
                    Ok(json_string) => {
                        self.output_area.set_text(json_string);
                        self.output_area.set_error(false);
                    }
                    Err(e) => {
                        self.output_area.set_error(true);
                        self.output_area
                            .set_error_label(format!("Conversion error: {}", e));
                    }
                },
                (ConfigFormat::Yaml, ConfigFormat::Toml) => match yaml_to_toml(&input_text) {
                    Ok(toml_string) => {
                        self.output_area.set_text(toml_string);
                        self.output_area.set_error(false);
                    }
                    Err(e) => {
                        self.output_area.set_error(true);
                        self.output_area
                            .set_error_label(format!("Conversion error: {}", e));
                    }
                },
                (ConfigFormat::Toml, ConfigFormat::Json) => match toml_to_json(&input_text) {
                    Ok(json_string) => {
                        self.output_area.set_text(json_string);
                        self.output_area.set_error(false);
                    }
                    Err(e) => {
                        self.output_area.set_error(true);
                        self.output_area
                            .set_error_label(format!("Conversion error: {}", e));
                    }
                },
                (ConfigFormat::Toml, ConfigFormat::Yaml) => match toml_to_yaml(&input_text) {
                    Ok(yaml_string) => {
                        self.output_area.set_text(yaml_string);
                        self.output_area.set_error(false);
                    }
                    Err(e) => {
                        self.output_area.set_error(true);
                        self.output_area
                            .set_error_label(format!("Conversion error: {}", e));
                    }
                },
                _ => {}
            }
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for ConfigFormatWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Initialize toggle groups
            let input_group = self.input_format_toggle_group.clone();
            let output_group = self.output_format_toggle_group.clone();
            let input_area = self.input_area.clone();
            let output_area = self.output_area.clone();
            glib::idle_add_local(move || {
                input_group.set_active(0);
                output_group.set_active(1);

                input_area.set_language("json");
                output_area.set_language("yaml");
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

            // Mark as initialized
            self.initialized.set(true);
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
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
