/*
 * cert_parse.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::prelude::ExpanderRowExt;
use adw::prelude::PreferencesGroupExt;
use adw::subclass::prelude::*;
use gettextrs::{gettext, pgettext};
use gtk::prelude::*;
use gtk::{gio, glib, glib::Properties, CompositeTemplate};

use crate::tools::cert_parse::parser;
use std::cell::RefCell;

mod imp {
    use adw::prelude::PreferencesRowExt;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/devtoolbox/tools/cert_parse/cert_parse.ui")]
    #[properties(wrapper_type = super::CertParseWidget)]
    pub struct CertParseWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        open_row: TemplateChild<adw::ActionRow>,

        #[template_child]
        file_path_label: TemplateChild<gtk::Label>,

        #[template_child]
        open_button: TemplateChild<gtk::Button>,

        #[template_child]
        view_stack: TemplateChild<adw::ViewStack>,

        #[template_child]
        certificate_group: TemplateChild<adw::PreferencesGroup>,

        #[template_child]
        button_content: TemplateChild<adw::ButtonContent>,

        #[template_child]
        version_label: TemplateChild<gtk::Label>,

        #[template_child]
        identity_label: TemplateChild<gtk::Label>,

        #[template_child]
        verifier_label: TemplateChild<gtk::Label>,

        #[template_child]
        not_before_label: TemplateChild<gtk::Label>,

        #[template_child]
        not_after_label: TemplateChild<gtk::Label>,

        #[template_child]
        serial_label: TemplateChild<gtk::Label>,

        #[template_child]
        general_group: TemplateChild<adw::PreferencesGroup>,

        #[template_child]
        named_extensions_group: TemplateChild<adw::PreferencesGroup>,

        #[template_child]
        extensions_group: TemplateChild<adw::PreferencesGroup>,

        #[template_child]
        open_file_dialog: TemplateChild<gtk::FileDialog>,

        // Properties
        #[property(set, get, nullable, type = gio::File)]
        file: RefCell<Option<gio::File>>,

        #[property(set, get, type = bool, default = false)]
        working: RefCell<bool>,

        // Other fields
        general_rows: RefCell<Vec<adw::ExpanderRow>>,
        named_extension_rows: RefCell<Vec<adw::ExpanderRow>>,
        other_extension_rows: RefCell<Vec<adw::ExpanderRow>>,
        is_expanded: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for CertParseWidget {
        const NAME: &'static str = "CertParseWidget";
        type Type = super::CertParseWidget;
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
    impl CertParseWidget {
        // Template callbacks and closures
        #[template_callback]
        async fn on_signal_clicked_open_button(&self) {
            self.open_button.set_sensitive(false);

            let filter_store = gio::ListStore::new::<gtk::FileFilter>();

            // Certificate only filter
            let certificate_filter = gtk::FileFilter::new();
            certificate_filter.set_name(Some(&pgettext("File filter", "Certificate Files")));
            for suffix in ["cer", "der", "pem"] {
                certificate_filter.add_suffix(suffix);
            }
            filter_store.append(&certificate_filter);

            // All files filter
            let all_files_filter = gtk::FileFilter::new();
            all_files_filter.set_name(Some(&pgettext("File filter", "All Files")));
            all_files_filter.add_pattern("*");
            filter_store.append(&all_files_filter);

            self.open_file_dialog.set_filters(Some(&filter_store));

            // Show dialog
            let result = self
                .open_file_dialog
                .open_future(Some(
                    &self.obj().root().and_downcast::<gtk::Window>().unwrap(),
                ))
                .await;

            // Handle result
            match result {
                Ok(file) => self.obj().set_file(Some(file)),
                Err(err) => {
                    let dismissed =
                        err.kind::<gtk::DialogError>() == Some(gtk::DialogError::Dismissed);
                    if !dismissed {
                        // Translator: {message} is replaced with the error message
                        let tmpl = pgettext("Error message", "Unable to open file: {message}");
                        let msg = tmpl.replace("{message}", &err.message());
                        self.obj().emit_by_name::<()>("error", &[&msg]);
                    }
                }
            }
            self.open_button.set_sensitive(true);
        }

        #[template_callback]
        fn on_signal_clicked_expand_button(&self) {
            let new_state = !*self.is_expanded.borrow();
            *self.is_expanded.borrow_mut() = new_state;

            if new_state {
                self.button_content.set_label(&gettext("Collapse All"));
                self.button_content.set_icon_name("up-symbolic");
            } else {
                self.button_content.set_label(&gettext("Expand All"));
                self.button_content.set_icon_name("down-symbolic");
            }

            for expander in self.general_rows.borrow().iter() {
                expander.set_expanded(new_state);
            }
            for expander in self.named_extension_rows.borrow().iter() {
                expander.set_expanded(new_state);
            }
            for expander in self.other_extension_rows.borrow().iter() {
                expander.set_expanded(new_state);
            }
        }

        // Other methods
        fn parse_file(&self, file: &gio::File) {
            let path = match file.peek_path() {
                Some(p) => p.to_path_buf(),
                None => {
                    self.show_error(&pgettext("Error message", "Cannot open file"));
                    return;
                }
            };

            let path_str = path.display().to_string();

            self.obj().set_working(true);

            let obj = self.obj().downgrade();
            glib::spawn_future_local(async move {
                // Read file in background thread
                let read_result = gio::spawn_blocking(move || -> Result<Vec<u8>, String> {
                    std::fs::read(&path).map_err(|e| {
                        let tmpl = pgettext("Error message", "Failed to read file: {message}");
                        tmpl.replace("{message}", &e.to_string())
                    })
                })
                .await;

                let Some(obj) = obj.upgrade() else { return };
                let imp = obj.imp();

                let data = match read_result {
                    Ok(Ok(d)) => d,
                    Ok(Err(e)) => {
                        imp.show_error(&e);
                        obj.set_working(false);
                        return;
                    }
                    Err(_) => {
                        imp.show_error(&pgettext(
                            "Error message",
                            "Failed to read file: unknown error",
                        ));
                        obj.set_working(false);
                        return;
                    }
                };

                // Parse in background thread
                let obj2 = obj.downgrade();
                let parse_result =
                    gio::spawn_blocking(move || parser::parse_certificate(&data)).await;

                let Some(obj) = obj2.upgrade() else { return };
                let imp = obj.imp();

                match parse_result {
                    Ok(Ok(result)) => {
                        imp.file_path_label.set_label(&path_str);
                        imp.populate_ui(result);
                    }
                    Ok(Err(e)) => {
                        imp.show_error(&e);
                        imp.file_path_label.set_label("");
                    }
                    Err(_) => {
                        imp.show_error(&pgettext(
                            "Error message",
                            "Certificate parsing failed unexpectedly",
                        ));
                        imp.file_path_label.set_label("");
                    }
                }

                obj.set_working(false);
            });
        }

        fn show_error(&self, message: &str) {
            self.view_stack.set_visible_child_name("empty");
            let toast = adw::Toast::new(message);
            toast.set_priority(adw::ToastPriority::High);
            self.toast_overlay.add_toast(toast);
        }

        fn empty_groups(&self) {
            for row in self.general_rows.borrow().iter() {
                self.general_group.remove(row);
            }
            self.general_rows.borrow_mut().clear();

            for row in self.named_extension_rows.borrow().iter() {
                self.named_extensions_group.remove(row);
            }
            self.named_extension_rows.borrow_mut().clear();

            for row in self.other_extension_rows.borrow().iter() {
                self.extensions_group.remove(row);
            }
            self.other_extension_rows.borrow_mut().clear();
        }

        fn populate_ui(&self, result: parser::CertParseResult) {
            // Clear old data
            self.empty_groups();
            *self.is_expanded.borrow_mut() = false;

            // Top-level info
            self.certificate_group.set_title(&result.identity);
            self.version_label.set_label(
                &pgettext("Certificate info", "Version: {version}")
                    .replace("{version}", &result.version),
            );
            self.identity_label.set_label(
                &pgettext("Certificate info", "Identity: {identity}")
                    .replace("{identity}", &result.identity),
            );
            self.verifier_label.set_label(
                &pgettext("Certificate info", "Verified by: {verifier}")
                    .replace("{verifier}", &result.verifier),
            );
            self.not_before_label.set_label(
                &pgettext("Certificate info", "Not before: {not_before_date}")
                    .replace("{not_before_date}", &result.not_before),
            );
            self.not_after_label.set_label(
                &pgettext("Certificate info", "Not after: {not_after_date}")
                    .replace("{not_after_date}", &result.not_after),
            );
            self.serial_label.set_label(
                &pgettext("Certificate info", "Serial: {serial}")
                    .replace("{serial}", &result.serial),
            );

            // Public key
            for section in &result.public_key_sections {
                let expander = self.create_expander(&section.title, &section.fields);
                self.general_group.add(&expander);
                self.general_rows.borrow_mut().push(expander);
            }

            // Signature algorithm
            let expander = self.create_expander(
                &result.signature_algorithm_section.title,
                &result.signature_algorithm_section.fields,
            );
            self.general_group.add(&expander);
            self.general_rows.borrow_mut().push(expander);

            // Signature value
            let expander = self.create_expander(
                &result.signature_value_section.title,
                &result.signature_value_section.fields,
            );
            self.general_group.add(&expander);
            self.general_rows.borrow_mut().push(expander);

            // Fingerprints
            let fp_fields = vec![
                parser::CertField {
                    label: "SHA1".to_string(),
                    value: parser::CertFieldValue::HexData(result.fingerprint_sha1),
                },
                parser::CertField {
                    label: "MD5".to_string(),
                    value: parser::CertFieldValue::HexData(result.fingerprint_md5),
                },
            ];
            let fp_expander =
                self.create_expander(&gettext("Certificate Fingerprints"), &fp_fields);
            self.general_group.add(&fp_expander);
            self.general_rows.borrow_mut().push(fp_expander);

            // General extensions
            for section in &result.general_extensions {
                let expander = self.create_expander(&section.title, &section.fields);
                self.general_group.add(&expander);
                self.general_rows.borrow_mut().push(expander);
            }

            // Named extensions
            for section in &result.named_extensions {
                let expander = self.create_expander(&section.title, &section.fields);
                self.named_extensions_group.add(&expander);
                self.named_extension_rows.borrow_mut().push(expander);
            }

            // Other extensions
            for section in &result.other_extensions {
                let expander = self.create_expander(&section.title, &section.fields);
                self.extensions_group.add(&expander);
                self.other_extension_rows.borrow_mut().push(expander);
            }

            self.view_stack.set_visible_child_name("certificate");
        }

        fn create_expander(&self, title: &str, fields: &[parser::CertField]) -> adw::ExpanderRow {
            let expander = adw::ExpanderRow::new();
            expander.set_title(title);

            let box_ = gtk::Box::new(gtk::Orientation::Vertical, 6);
            box_.set_margin_top(6);
            box_.set_margin_bottom(6);
            box_.set_margin_start(12);

            for field in fields {
                let value_str = match &field.value {
                    parser::CertFieldValue::Text(text) => text.clone(),
                    parser::CertFieldValue::HexData(data) => {
                        parser::format_hex_data(data, 10, &field.label)
                    }
                    parser::CertFieldValue::List(items) => {
                        let indent = " ".repeat(field.label.len() + 6);
                        let mut result = String::new();
                        for (i, item) in items.iter().enumerate() {
                            if i > 0 {
                                result.push_str(&format!(",\n{indent}{item}"));
                            } else {
                                result.push_str(item);
                            }
                        }
                        result
                    }
                };

                let label = gtk::Label::new(None);
                label.set_markup(&format!(
                    "{label}: {value}",
                    label = glib::markup_escape_text(&field.label),
                    value = glib::markup_escape_text(&value_str),
                ));
                label.set_halign(gtk::Align::Start);
                label.set_selectable(true);
                label.add_css_class("monospace");
                box_.append(&label);
            }

            expander.add_row(&box_);
            expander.set_expanded(*self.is_expanded.borrow());

            expander
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for CertParseWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.obj()
                .bind_property("working", &*self.open_button, "sensitive")
                .sync_create()
                .transform_to(|_, working: bool| Some(!working))
                .build();

            // File changes
            let obj = self.obj().clone();
            obj.connect_notify_local(Some("file"), move |widget, _param_spec| {
                let file = widget.imp().file.borrow().clone();
                // println!("{:?}", file.unwrap().peek_path());
                if let Some(file) = file {
                    widget.imp().parse_file(&file);
                }
            });
        }
    }

    impl WidgetImpl for CertParseWidget {}
    impl BinImpl for CertParseWidget {}
}

glib::wrapper! {
    pub struct CertParseWidget(ObjectSubclass<imp::CertParseWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl CertParseWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
