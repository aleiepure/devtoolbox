/*
 * number_bases.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, CompositeTemplate};

use std::cell::RefCell;

use crate::tools::number_bases::conversion::{do_conversion, Base};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/number_bases/number_bases.ui")]
    pub struct NumberBasesWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        decimal_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        binary_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        hexadecimal_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        octal_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        ascii_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        utf8_entryrow: TemplateChild<adw::EntryRow>,

        // Other fields
        decimal_signal_id: RefCell<Option<glib::SignalHandlerId>>,
        binary_signal_id: RefCell<Option<glib::SignalHandlerId>>,
        hexadecimal_signal_id: RefCell<Option<glib::SignalHandlerId>>,
        octal_signal_id: RefCell<Option<glib::SignalHandlerId>>,
        ascii_signal_id: RefCell<Option<glib::SignalHandlerId>>,
        utf8_signal_id: RefCell<Option<glib::SignalHandlerId>>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for NumberBasesWidget {
        const NAME: &'static str = "NumberBasesWidget";
        type Type = super::NumberBasesWidget;
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
    impl NumberBasesWidget {
        fn do_convert(&self, input_base: Base) {
            let input_text = match input_base {
                Base::Decimal => self.decimal_entryrow.text().to_string(),
                Base::Binary => self.binary_entryrow.text().to_string(),
                Base::Octal => self.octal_entryrow.text().to_string(),
                Base::Hexadecimal => self.hexadecimal_entryrow.text().to_string(),
                Base::Ascii => self.ascii_entryrow.text().to_string(),
                Base::Utf8 => self.utf8_entryrow.text().to_string(),
            };

            let result = do_conversion(&input_text, input_base);

            let is_error = !input_text.is_empty()
                && result.decimal.is_empty()
                && result.binary.is_empty()
                && result.octal.is_empty()
                && result.hexadecimal.is_empty()
                && result.ascii.is_empty()
                && result.utf8.is_empty();

            // Get the active entry row widget to add/remove error class
            let active_widget = match input_base {
                Base::Decimal => self.decimal_entryrow.upcast_ref::<gtk::Widget>(),
                Base::Binary => self.binary_entryrow.upcast_ref::<gtk::Widget>(),
                Base::Octal => self.octal_entryrow.upcast_ref::<gtk::Widget>(),
                Base::Hexadecimal => self.hexadecimal_entryrow.upcast_ref::<gtk::Widget>(),
                Base::Ascii => self.ascii_entryrow.upcast_ref::<gtk::Widget>(),
                Base::Utf8 => self.utf8_entryrow.upcast_ref::<gtk::Widget>(),
            };

            if is_error {
                active_widget.add_css_class("error");
            } else {
                active_widget.remove_css_class("error");
            }

            self.block_signals();

            if !matches!(input_base, Base::Decimal) {
                self.decimal_entryrow.set_text(&result.decimal);
            }
            if !matches!(input_base, Base::Binary) {
                self.binary_entryrow.set_text(&result.binary);
            }
            if !matches!(input_base, Base::Octal) {
                self.octal_entryrow.set_text(&result.octal);
            }
            if !matches!(input_base, Base::Hexadecimal) {
                self.hexadecimal_entryrow.set_text(&result.hexadecimal);
            }
            if !matches!(input_base, Base::Ascii) {
                self.ascii_entryrow.set_text(&result.ascii);
            }
            if !matches!(input_base, Base::Utf8) {
                self.utf8_entryrow.set_text(&result.utf8);
            }

            self.unblock_signals();
        }

        fn block_signals(&self) {
            if let Some(id) = self.decimal_signal_id.borrow().as_ref() {
                self.decimal_entryrow.block_signal(id);
            }
            if let Some(id) = self.binary_signal_id.borrow().as_ref() {
                self.binary_entryrow.block_signal(id);
            }
            if let Some(id) = self.octal_signal_id.borrow().as_ref() {
                self.octal_entryrow.block_signal(id);
            }
            if let Some(id) = self.hexadecimal_signal_id.borrow().as_ref() {
                self.hexadecimal_entryrow.block_signal(id);
            }
            if let Some(id) = self.ascii_signal_id.borrow().as_ref() {
                self.ascii_entryrow.block_signal(id);
            }
            if let Some(id) = self.utf8_signal_id.borrow().as_ref() {
                self.utf8_entryrow.block_signal(id);
            }
        }

        fn unblock_signals(&self) {
            if let Some(id) = self.decimal_signal_id.borrow().as_ref() {
                self.decimal_entryrow.unblock_signal(id);
            }
            if let Some(id) = self.binary_signal_id.borrow().as_ref() {
                self.binary_entryrow.unblock_signal(id);
            }
            if let Some(id) = self.octal_signal_id.borrow().as_ref() {
                self.octal_entryrow.unblock_signal(id);
            }
            if let Some(id) = self.hexadecimal_signal_id.borrow().as_ref() {
                self.hexadecimal_entryrow.unblock_signal(id);
            }
            if let Some(id) = self.ascii_signal_id.borrow().as_ref() {
                self.ascii_entryrow.unblock_signal(id);
            }
            if let Some(id) = self.utf8_signal_id.borrow().as_ref() {
                self.utf8_entryrow.unblock_signal(id);
            }
        }
    }

    impl ObjectImpl for NumberBasesWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Connect signals. Done here to have access to signal handler IDs
            let signal_id = self.decimal_entryrow.connect_changed(glib::clone!(
                #[weak(rename_to = this)]
                self,
                move |_| {
                    this.do_convert(Base::Decimal);
                }
            ));
            self.decimal_signal_id.replace(Some(signal_id));

            let signal_id = self.binary_entryrow.connect_changed(glib::clone!(
                #[weak(rename_to = this)]
                self,
                move |_| {
                    this.do_convert(Base::Binary);
                }
            ));
            self.binary_signal_id.replace(Some(signal_id));

            let signal_id = self.octal_entryrow.connect_changed(glib::clone!(
                #[weak(rename_to = this)]
                self,
                move |_| {
                    this.do_convert(Base::Octal);
                }
            ));
            self.octal_signal_id.replace(Some(signal_id));

            let signal_id = self.hexadecimal_entryrow.connect_changed(glib::clone!(
                #[weak(rename_to = this)]
                self,
                move |_| {
                    this.do_convert(Base::Hexadecimal);
                }
            ));
            self.hexadecimal_signal_id.replace(Some(signal_id));

            let signal_id = self.ascii_entryrow.connect_changed(glib::clone!(
                #[weak(rename_to = this)]
                self,
                move |_| {
                    this.do_convert(Base::Ascii);
                }
            ));
            self.ascii_signal_id.replace(Some(signal_id));

            let signal_id = self.utf8_entryrow.connect_changed(glib::clone!(
                #[weak(rename_to = this)]
                self,
                move |_| {
                    this.do_convert(Base::Utf8);
                }
            ));
            self.utf8_signal_id.replace(Some(signal_id));
        }
    }

    impl WidgetImpl for NumberBasesWidget {}
    impl BinImpl for NumberBasesWidget {}
}

glib::wrapper! {
    pub struct NumberBasesWidget(ObjectSubclass<imp::NumberBasesWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl NumberBasesWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
