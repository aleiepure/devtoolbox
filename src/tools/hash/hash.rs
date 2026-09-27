/*
 * hash.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::prelude::ActionRowExt;
use adw::subclass::prelude::*;
use gettextrs::pgettext;
use gtk::gio;
use gtk::prelude::*;
use gtk::{glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

#[derive(Debug, Clone, Copy)]
pub enum HashAlgorithm {
    MD5,
    SHA1,
    SHA256,
    SHA512,
    SHA3_256,
    SHA3_512,
    BLAKE3,
}

fn feed_stream(stream: &gio::FileInputStream, consume: &mut dyn FnMut(&[u8])) -> bool {
    let mut buffer = [0u8; 64 * 1024];
    loop {
        match stream.read(&mut buffer, gio::Cancellable::NONE) {
            Ok(0) => return true, // EOF
            Ok(n) => consume(&buffer[..n]),
            Err(_) => return false,
        }
    }
}

mod imp {

    use adw::prelude::ComboRowExt;
    use digest::{Digest, DynDigest};
    use gettextrs::gettext;

    use crate::core::widgets::ActionableEntryRow;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/devtoolbox/tools/hash/hash.ui")]
    #[properties(wrapper_type = super::HashWidget)]
    pub struct HashWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,
        #[template_child]
        open_row: TemplateChild<adw::ActionRow>,
        #[template_child]
        open_button: TemplateChild<gtk::Button>,
        #[template_child]
        open_file_dialog: TemplateChild<gtk::FileDialog>,
        #[template_child]
        validation_group: TemplateChild<adw::PreferencesGroup>,

        #[template_child]
        md5_row: TemplateChild<ActionableEntryRow>,
        #[template_child]
        sha1_row: TemplateChild<ActionableEntryRow>,
        #[template_child]
        sha256_row: TemplateChild<ActionableEntryRow>,
        #[template_child]
        sha512_row: TemplateChild<ActionableEntryRow>,
        #[template_child]
        sha3_256_row: TemplateChild<ActionableEntryRow>,
        #[template_child]
        sha3_512_row: TemplateChild<ActionableEntryRow>,
        #[template_child]
        blake3_row: TemplateChild<ActionableEntryRow>,

        #[template_child]
        validation_switch_row: TemplateChild<adw::SwitchRow>,
        #[template_child]
        validation_algorithm_row: TemplateChild<adw::ComboRow>,
        #[template_child]
        validation_hash_row: TemplateChild<ActionableEntryRow>,

        // Properties
        /// The file to compute the hash for
        #[property(set, get, nullable, type = gio::File)]
        file: RefCell<Option<gio::File>>,

        /// Validation status: the computed hash matches the known hash
        #[property(set, get, type = bool, default = false)]
        validation_valid: RefCell<bool>,

        /// Validation status: the computed hash does not match the known hash
        #[property(set, get, type = bool, default = false)]
        validation_invalid: RefCell<bool>,

        /// Validation status: the hash calculation is still running
        #[property(set, get, type = bool, default = false)]
        validation_pending: RefCell<bool>,

        // Other fields
        generation: RefCell<u64>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for HashWidget {
        const NAME: &'static str = "HashWidget";
        type Type = super::HashWidget;
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
    impl HashWidget {
        // Template callbacks and closures
        #[template_callback]
        async fn on_signal_clicked_open_button(&self) {
            self.open_button.set_sensitive(false);

            let filter_store = gio::ListStore::new::<gtk::FileFilter>();
            let all_files_filter = gtk::FileFilter::new();
            all_files_filter.set_name(Some(&pgettext("File filter", "All Files")));
            all_files_filter.add_pattern("*");
            filter_store.append(&all_files_filter);

            self.open_file_dialog.set_filters(Some(&filter_store));

            // show dialog
            let result = self
                .open_file_dialog
                .open_future(Some(
                    &self.obj().root().and_downcast::<gtk::Window>().unwrap(),
                ))
                .await;

            // Handle the result
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

        // Other methods
        fn calculate_hashes(&self, file: &gio::File) {
            let generation = {
                let mut gen = self.generation.borrow_mut();
                *gen += 1;
                *gen
            };

            let rows = [
                (self.md5_row.get(), HashAlgorithm::MD5),
                (self.sha1_row.get(), HashAlgorithm::SHA1),
                (self.sha256_row.get(), HashAlgorithm::SHA256),
                (self.sha512_row.get(), HashAlgorithm::SHA512),
                (self.sha3_256_row.get(), HashAlgorithm::SHA3_256),
                (self.sha3_512_row.get(), HashAlgorithm::SHA3_512),
                (self.blake3_row.get(), HashAlgorithm::BLAKE3),
            ];

            for (row, algorithm) in rows {
                row.set_working(true);
                row.set_text(&gettext("Computing..."));

                let file = file.clone();
                let obj = self.obj().downgrade();

                glib::spawn_future_local(async move {
                    let hash =
                        gio::spawn_blocking(move || Self::calculate_hash(&file, algorithm)).await;

                    let Some(obj) = obj.upgrade() else {
                        return;
                    };
                    let imp = obj.imp();

                    // discard if a newer file was opened while computing
                    if *imp.generation.borrow() != generation {
                        return;
                    }

                    row.set_working(false);
                    if let Ok(hash) = hash {
                        row.set_text(&hash);
                    }
                    imp.evaluate_validation();
                });
            }

            self.evaluate_validation();
        }

        fn calculate_hash(file: &gio::File, algorithm: HashAlgorithm) -> String {
            let input_stream = match file.read(gio::Cancellable::NONE) {
                Ok(stream) => stream,
                Err(_) => return String::new(),
            };

            match algorithm {
                HashAlgorithm::BLAKE3 => {
                    let mut hasher = blake3::Hasher::new();
                    if !feed_stream(&input_stream, &mut |chunk| {
                        hasher.update(chunk);
                    }) {
                        return String::new();
                    }
                    hasher.finalize().to_hex().to_string()
                }
                _ => {
                    let mut hasher: Box<dyn DynDigest> = match algorithm {
                        HashAlgorithm::MD5 => Box::new(md5::Md5::new()),
                        HashAlgorithm::SHA1 => Box::new(sha1::Sha1::new()),
                        HashAlgorithm::SHA256 => Box::new(sha2::Sha256::new()),
                        HashAlgorithm::SHA512 => Box::new(sha2::Sha512::new()),
                        HashAlgorithm::SHA3_256 => Box::new(sha3::Sha3_256::new()),
                        HashAlgorithm::SHA3_512 => Box::new(sha3::Sha3_512::new()),
                        HashAlgorithm::BLAKE3 => unreachable!(),
                    };
                    if !feed_stream(&input_stream, &mut |chunk| hasher.update(chunk)) {
                        return String::new();
                    }
                    hex::encode(hasher.finalize())
                }
            }
        }

        fn evaluate_validation(&self) {
            let input = self.validation_hash_row.text();
            let input = input.trim();

            // Ignore if input is empty
            if !self.validation_switch_row.is_active() || input.is_empty() {
                self.obj().set_validation_valid(false);
                self.obj().set_validation_invalid(false);
                self.obj().set_validation_pending(false);
                return;
            }

            let row = match self.validation_algorithm_row.selected() {
                0 => self.md5_row.get(),
                1 => self.sha1_row.get(),
                2 => self.sha256_row.get(),
                3 => self.sha512_row.get(),
                4 => self.sha3_256_row.get(),
                5 => self.sha3_512_row.get(),
                6 => self.blake3_row.get(),
                _ => {
                    self.obj().set_validation_valid(false);
                    self.obj().set_validation_invalid(false);
                    self.obj().set_validation_pending(false);
                    return;
                }
            };

            // algorithm is pending
            if row.working() {
                self.obj().set_validation_valid(false);
                self.obj().set_validation_invalid(false);
                self.obj().set_validation_pending(true);
                return;
            }

            // compare case insensitively
            let matches =
                !row.text().is_empty() && row.text().to_lowercase() == input.to_lowercase();

            self.obj().set_validation_valid(matches);
            self.obj().set_validation_invalid(!matches);
            self.obj().set_validation_pending(false);
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for HashWidget {
        fn constructed(&self) {
            self.parent_constructed();

            let obj = self.obj().clone();
            obj.connect_notify_local(Some("file"), move |widget, _param_spec| {
                let file = widget.imp().file.borrow().clone();
                if let Some(file) = file {
                    let path = match file.peek_path() {
                        Some(p) => p.to_path_buf(),
                        _ => return,
                    };

                    let path_str = path.display().to_string();

                    widget.imp().validation_group.set_visible(true);
                    widget.imp().open_row.set_subtitle(&path_str);
                    widget.imp().calculate_hashes(&file);
                }
            });

            let obj = self.obj().clone();
            self.validation_switch_row
                .connect_notify_local(Some("active"), move |_, _| {
                    obj.imp().evaluate_validation();
                });

            let obj = self.obj().clone();
            self.validation_algorithm_row
                .connect_notify_local(Some("selected"), move |_, _| {
                    obj.imp().evaluate_validation();
                });

            let obj = self.obj().clone();
            self.validation_hash_row
                .connect_notify_local(Some("text"), move |_, _| {
                    obj.imp().evaluate_validation();
                });
        }
    }

    impl WidgetImpl for HashWidget {}
    impl BinImpl for HashWidget {}
}

glib::wrapper! {
    pub struct HashWidget(ObjectSubclass<imp::HashWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl HashWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
