/*
 * cron_parser.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, CompositeTemplate};

use crate::{
    core::widgets::{ActionableEntryRow, TextArea},
    tools::cron_parser::SpecifierRow,
};

mod imp {
    use chrono::Utc;
    use cron::Schedule;
    use gettextrs::gettext;
    use std::str::FromStr;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/cron_parser/cron_parser.ui")]
    pub struct CronParserWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        popover_toast: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        output_length_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        output_format_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        expression_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        text_area: TemplateChild<TextArea>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for CronParserWidget {
        const NAME: &'static str = "CronParserWidget";
        type Type = super::CronParserWidget;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            SpecifierRow::ensure_type();
            klass.bind_template();
            klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl CronParserWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_copied_specifier(&self, _specifier: &str) {
            let toast = adw::Toast::builder()
                .title(gettext("Copied to Clipboard"))
                .build();
            self.popover_toast.add_toast(toast);
        }

        #[template_callback]
        fn on_signal_notify_value_spinrow(&self) {
            self.do_parsing();
        }

        #[template_callback]
        fn on_signal_notify_value_format_entryrow(&self) {
            self.do_parsing();
        }

        #[template_callback]
        fn on_signal_changed_expression_entryrow(&self) {
            self.do_parsing();
        }

        // Other methods
        fn do_parsing(&self) {
            let format = self.output_format_entryrow.text();
            if format.is_empty() {
                self.output_format_entryrow.add_css_class("error");
                self.text_area.set_text(String::new());
                return;
            }

            let expression = self.expression_entryrow.text().to_string();
            let expression = if expression.split_whitespace().count() == 5 {
                format!("0 {}", expression)
            } else {
                expression
            };

            let schedule = match Schedule::from_str(&expression) {
                Ok(s) => {
                    self.expression_entryrow.remove_css_class("error");
                    s
                }
                Err(_err) => {
                    self.expression_entryrow.add_css_class("error");
                    self.text_area.set_text(String::new());
                    return;
                }
            };

            let mut lines = String::new();
            let mut format_valid = true;

            for datetime in schedule
                .upcoming(Utc)
                .take(self.output_length_spinrow.value() as usize)
            {
                let result =
                    std::panic::catch_unwind(|| datetime.format(format.as_str()).to_string());

                match result {
                    Ok(line) => {
                        lines.push_str(&line);
                        lines.push('\n');
                    }
                    Err(_) => {
                        format_valid = false;
                        break;
                    }
                }
            }

            if format_valid {
                self.output_format_entryrow.remove_css_class("error");
                self.text_area.set_text(lines);
            } else {
                self.output_format_entryrow.add_css_class("error");
                self.text_area.set_text(String::new());
            }
        }
    }

    impl ObjectImpl for CronParserWidget {
        fn constructed(&self) {
            self.parent_constructed();
            self.do_parsing();
        }
    }

    impl WidgetImpl for CronParserWidget {}
    impl BinImpl for CronParserWidget {}
}

glib::wrapper! {
    pub struct CronParserWidget(ObjectSubclass<imp::CronParserWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl CronParserWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
