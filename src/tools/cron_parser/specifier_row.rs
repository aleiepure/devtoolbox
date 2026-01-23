/*
 * specifier_row.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gettextrs::gettext;
use gtk::prelude::*;
use gtk::{gdk::Display, glib, glib::subclass::Signal, glib::Properties, CompositeTemplate};

use std::cell::RefCell;
use std::sync::OnceLock;

// MARK: Implementation
mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/cron_parser/specifier_row.ui")]
    #[properties(wrapper_type = super::SpecifierRow, )]
    pub struct SpecifierRow {
        // MARK: Template widgets
        #[template_child]
        button: TemplateChild<gtk::Button>,

        // MARK: Properties
        /// Specifier string
        #[property(set, get, type = String, default = "")]
        specifier: RefCell<String>,

        /// Specifier description
        #[property(set, get, type = String, default = "")]
        specifier_description: RefCell<String>,

        /// Specifier example
        /// String will be automatically prefixed with "Example: " in the user's
        /// locale. Only valid if `hide_example` is false.
        #[property(set, get, type = String, default = "")]
        specifier_example: RefCell<String>,

        /// Hide example. If true, the example label will be hidden.
        #[property(set, get, type = bool, default = false)]
        hide_example: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for SpecifierRow {
        const NAME: &'static str = "SpecifierRow";
        type Type = super::SpecifierRow;
        type ParentType = adw::ActionRow;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl SpecifierRow {
        // MARK: Signal handlers
        ///Button clicked, emits "copied" signal
        #[template_callback]
        fn on_signal_clicked_button(&self) {
            let clipboard = Display::default().unwrap().clipboard();
            clipboard.set_text(&self.specifier.borrow());
            self.obj()
                .emit_by_name::<()>("copied", &[&self.specifier.borrow().as_str()]);
        }

        #[template_callback]
        fn build_example_closure(&self, example: &str, hide: bool) -> String {
            if example.is_empty() || hide {
                return String::new();
            }

            format!("{}: {}", gettext("Example"), example)
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for SpecifierRow {
        // MARK: Construction
        fn constructed(&self) {
            self.parent_constructed();
        }

        // MARK: Signals
        fn signals() -> &'static [Signal] {
            static SIGNALS: OnceLock<Vec<Signal>> = OnceLock::new();
            SIGNALS.get_or_init(|| {
                vec![Signal::builder("copied")
                    .param_types([String::static_type()])
                    .build()]
            })
        }
    }

    impl WidgetImpl for SpecifierRow {}
    impl ListBoxRowImpl for SpecifierRow {}
    impl PreferencesRowImpl for SpecifierRow {}
    impl ActionRowImpl for SpecifierRow {}
}

// MARK: Wrapper
glib::wrapper! {
    pub struct SpecifierRow(ObjectSubclass<imp::SpecifierRow>)
        @extends adw::ActionRow, adw::PreferencesRow, gtk::ListBoxRow, gtk::Widget,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Actionable;
}

// MARK: Widget
impl SpecifierRow {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
