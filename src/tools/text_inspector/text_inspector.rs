/*
 * text_inspector.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::{connect_imp_signal, connect_imp_signals};
use crate::{core::widgets::TextArea, tools::text_inspector::string_cases::StringCase};
use adw::prelude::ComboRowExt;
use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, CompositeTemplate};

use std::cell::RefCell;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/text_inspector/text_inspector.ui")]
    pub struct TextInspectorWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        case_comborow: TemplateChild<adw::ComboRow>,

        #[template_child]
        line_label: TemplateChild<gtk::Label>,

        #[template_child]
        column_label: TemplateChild<gtk::Label>,

        #[template_child]
        characters_label: TemplateChild<gtk::Label>,

        #[template_child]
        words_label: TemplateChild<gtk::Label>,

        #[template_child]
        lines_label: TemplateChild<gtk::Label>,

        #[template_child]
        text_area: TemplateChild<TextArea>,

        // Other fields
        text_area_changed_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        case_comborow_notify_selected_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        original_text: RefCell<String>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for TextInspectorWidget {
        const NAME: &'static str = "TextInspectorWidget";
        type Type = super::TextInspectorWidget;
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
    impl TextInspectorWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_selected_case_comborow(&self) {
            if self.text_area.text().len() == 0 {
                return;
            }

            let selected = self.case_comborow.selected();
            let original_text = self.original_text.borrow().clone();

            if let Some(handler_id) = self.text_area_changed_signal_handler_id.borrow().as_ref() {
                self.text_area.block_signal(handler_id);

                match selected {
                    0 => self.text_area.set_text(original_text), // None
                    1 => self.text_area.set_text(original_text.to_sentence_case()),
                    2 => self.text_area.set_text(original_text.to_lowercase()),
                    3 => self.text_area.set_text(original_text.to_uppercase()),
                    4 => self.text_area.set_text(original_text.to_title_case()),
                    5 => self.text_area.set_text(original_text.to_camel_case()),
                    6 => self.text_area.set_text(original_text.to_pascal_case()),
                    7 => self.text_area.set_text(original_text.to_snake_case()),
                    8 => self.text_area.set_text(original_text.to_constant_case()),
                    9 => self.text_area.set_text(original_text.to_kebab_case()),
                    10 => self.text_area.set_text(original_text.to_cobol_case()),
                    11 => self.text_area.set_text(original_text.to_train_case()),
                    12 => self.text_area.set_text(original_text.to_dot_case()),
                    13 => self.text_area.set_text(original_text.to_alternating_case()),
                    14 => self
                        .text_area
                        .set_text(original_text.to_reverse_alternating_case()),
                    _ => unreachable!(),
                }

                self.text_area.unblock_signal(handler_id);
            }

            self.calculate_statistics();
        }

        #[template_callback]
        fn on_signal_changed_text_area(&self) {
            // Reset case_comborow to "None".
            // New text becomes the new "original" case.
            if let Some(handler_id) = self
                .case_comborow_notify_selected_signal_handler_id
                .borrow()
                .as_ref()
            {
                self.case_comborow.block_signal(handler_id);
                self.case_comborow.set_selected(0);
                self.case_comborow.unblock_signal(handler_id);
            }

            let text = self.text_area.text();
            self.original_text.replace(text.clone());

            self.calculate_statistics();
        }

        #[template_callback]
        fn on_signal_cursor_moved_text_area(&self) {
            let insert_mark = self.text_area.buffer().get_insert();
            let iter = self.text_area.buffer().iter_at_mark(&insert_mark);
            self.line_label.set_label(&(iter.line() + 1).to_string());
            self.column_label
                .set_label(&(iter.line_offset() + 1).to_string());
        }

        // Other methods
        fn calculate_statistics(&self) {
            self.characters_label
                .set_label(&self.text_area.text().chars().count().to_string());
            self.words_label
                .set_label(&self.text_area.text().split_whitespace().count().to_string());
            self.lines_label
                .set_label(&self.text_area.text().lines().count().to_string());
        }
    }

    impl ObjectImpl for TextInspectorWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Connect signals
            connect_imp_signals!(self;
                text_area_changed_signal_handler_id <= text_area, "changed" => on_signal_changed_text_area;
                case_comborow_notify_selected_signal_handler_id <= case_comborow, "notify::selected" => on_signal_notify_selected_case_comborow
            );
        }
    }

    impl WidgetImpl for TextInspectorWidget {}
    impl BinImpl for TextInspectorWidget {}
}

glib::wrapper! {
    pub struct TextInspectorWidget(ObjectSubclass<imp::TextInspectorWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl TextInspectorWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
