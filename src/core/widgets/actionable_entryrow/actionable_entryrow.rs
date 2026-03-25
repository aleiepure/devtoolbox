/*
 * text_area.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gdk::Display, glib, glib::subclass::Signal, glib::Properties, CompositeTemplate};

use std::cell::RefCell;
use std::sync::OnceLock;

// MARK: Implementation
mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(
        resource = "/me/iepure/devtoolbox/core/widgets/actionable_entryrow/actionable_entryrow.ui"
    )]
    #[properties(wrapper_type = super::ActionableEntryRow, )]
    pub struct ActionableEntryRow {
        // MARK: Template widgets
        #[template_child]
        generate_button: TemplateChild<gtk::Button>,

        #[template_child]
        copy_button: TemplateChild<gtk::Button>,

        #[template_child]
        paste_button: TemplateChild<gtk::Button>,

        #[template_child]
        clear_button: TemplateChild<gtk::Button>,

        // MARK: Properties
        /// Generate button visibility
        #[property(set, get, type = bool, default = false)]
        generate_button_visible: RefCell<bool>,

        /// Copy button visibility
        #[property(set, get, type = bool, default = false)]
        copy_button_visible: RefCell<bool>,

        /// Paste button visibility
        #[property(set, get, type = bool, default = false)]
        paste_button_visible: RefCell<bool>,

        /// Clear button visibility
        #[property(set, get, type = bool, default = false)]
        clear_button_visible: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for ActionableEntryRow {
        const NAME: &'static str = "ActionableEntryRow";
        type Type = super::ActionableEntryRow;
        type ParentType = adw::EntryRow;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl ActionableEntryRow {
        // MARK: Signal handlers
        /// Generate button clicked, emits "generate" signal
        #[template_callback]
        fn on_signal_clicked_generate_button(&self) {
            self.obj().emit_by_name::<()>("generate", &[]);
        }

        /// Copy button clicked, copies the entry text to clipboard
        #[template_callback]
        fn on_signal_clicked_copy_button(&self) {
            let text = self.obj().text();
            let clipboard = Display::default().unwrap().clipboard();
            clipboard.set_text(&text);
        }

        /// Paste button clicked, pastes the clipboard text to the entry
        #[template_callback]
        async fn on_signal_clicked_paste_button(&self) {
            let clipboard = Display::default().unwrap().clipboard();
            let result = clipboard.read_text_future().await;
            match result {
                Ok(text) => {
                    self.obj().set_text(text.unwrap().as_str());
                }
                Err(err) => {
                    eprintln!("Failed to read clipboard text: {}", err);
                }
            }
        }

        #[template_callback]
        fn on_signal_clicked_clear_button(&self) {
            self.obj().set_text("");
            self.obj().emit_by_name::<()>("cleared", &[]);
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for ActionableEntryRow {
        // MARK: Construction
        fn constructed(&self) {
            self.parent_constructed();
        }

        // MARK: Signals
        fn signals() -> &'static [Signal] {
            static SIGNALS: OnceLock<Vec<Signal>> = OnceLock::new();
            SIGNALS.get_or_init(|| {
                vec![
                    Signal::builder("generate").build(),
                    Signal::builder("cleared").build(),
                ]
            })
        }
    }

    impl WidgetImpl for ActionableEntryRow {}
    impl ListBoxRowImpl for ActionableEntryRow {}
    impl PreferencesRowImpl for ActionableEntryRow {}
    impl EntryRowImpl for ActionableEntryRow {}
}

// MARK: Wrapper
glib::wrapper! {
    pub struct ActionableEntryRow(ObjectSubclass<imp::ActionableEntryRow>)
        @extends adw::EntryRow, adw::PreferencesRow, gtk::ListBoxRow, gtk::Widget,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Editable, gtk::Actionable;
}

// MARK: Widget
impl ActionableEntryRow {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
