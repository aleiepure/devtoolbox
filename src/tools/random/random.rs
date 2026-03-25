/*
 * random.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, CompositeTemplate};

use crate::core::widgets::ActionableEntryRow;

use rand::prelude::SliceRandom;
use rand::Rng;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/random/random.ui")]
    pub struct RandomWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        string_length_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        string_uppercase_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        string_lowercase_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        string_numbers_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        string_symbols_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        string_min_numbers_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        string_min_symbols_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        string_avoid_ambiguous_switchrow: TemplateChild<adw::SwitchRow>,

        #[template_child]
        string_result_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        number_min_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        number_max_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        number_result_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        passphrase_length_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        passphrase_separator_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        passphrase_capitalize_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        passphrase_include_number_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        passphrase_result_entryrow: TemplateChild<ActionableEntryRow>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for RandomWidget {
        const NAME: &'static str = "RandomWidget";
        type Type = super::RandomWidget;
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
    impl RandomWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_value_string_length_spinrow(&self) {
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_toggled_string_uppercase_checkbutton(&self) {
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_toggled_string_lowercase_checkbutton(&self) {
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_toggled_string_numbers_checkbutton(&self) {
            if self.string_numbers_checkbutton.is_active() {
                if self.string_min_numbers_spinrow.value() == 0.0 {
                    self.string_min_numbers_spinrow.set_value(1.0);
                }
            } else {
                self.string_min_numbers_spinrow.set_value(0.0);
            }
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_toggled_string_symbols_checkbutton(&self) {
            if self.string_symbols_checkbutton.is_active() {
                if self.string_min_symbols_spinrow.value() == 0.0 {
                    self.string_min_symbols_spinrow.set_value(1.0);
                }
            } else {
                self.string_min_symbols_spinrow.set_value(0.0);
            }
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_notify_value_string_min_numbers_spinrow(&self) {
            if self.string_min_numbers_spinrow.value() == 0.0 {
                self.string_numbers_checkbutton.set_active(false);
            } else {
                self.string_numbers_checkbutton.set_active(true);
            }
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_notify_value_string_min_symbols_spinrow(&self) {
            if self.string_min_symbols_spinrow.value() == 0.0 {
                self.string_symbols_checkbutton.set_active(false);
            } else {
                self.string_symbols_checkbutton.set_active(true);
            }
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_notify_active_string_avoid_ambiguous_switchrow(&self) {
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_clicked_string_result_entryrow_generate_button(&self) {
            self.update_string_result();
        }

        #[template_callback]
        fn on_signal_notify_value_number_min_spinrow(&self) {
            let min = self.number_min_spinrow.value();
            let max = self.number_max_spinrow.value();
            if min > max {
                self.number_max_spinrow.set_value(min);
            }
            self.update_number_result();
        }

        #[template_callback]
        fn on_signal_notify_value_number_max_spinrow(&self) {
            let min = self.number_min_spinrow.value();
            let max = self.number_max_spinrow.value();
            if max < min {
                self.number_min_spinrow.set_value(max);
            }
            self.update_number_result();
        }

        #[template_callback]
        fn on_signal_clicked_number_result_entryrow_generate_button(&self) {
            self.update_number_result();
        }

        #[template_callback]
        fn on_signal_notify_value_passphrase_length_spinrow(&self) {
            self.update_passphrase_result();
        }

        #[template_callback]
        fn on_signal_changed_passphrase_separator_entryrow(&self) {
            self.update_passphrase_result();
        }

        #[template_callback]
        fn on_signal_toggled_passphrase_capitalize_checkbutton(&self) {
            self.update_passphrase_result();
        }

        #[template_callback]
        fn on_signal_toggled_passphrase_include_number_checkbutton(&self) {
            self.update_passphrase_result();
        }

        #[template_callback]
        fn on_signal_clicked_passphrase_result_entryrow_generate_button(&self) {
            self.update_passphrase_result();
        }

        // Other methods
        fn update_string_result(&self) {
            let length = self.string_length_spinrow.value() as usize;
            let include_uppercase = self.string_uppercase_checkbutton.is_active();
            let include_lowercase = self.string_lowercase_checkbutton.is_active();
            let include_numbers = self.string_numbers_checkbutton.is_active();
            let include_symbols = self.string_symbols_checkbutton.is_active();
            let min_numbers = self.string_min_numbers_spinrow.value() as usize;
            let min_symbols = self.string_min_symbols_spinrow.value() as usize;
            let avoid_ambiguous = self.string_avoid_ambiguous_switchrow.is_active();

            // Nothing selected, clear output
            if !include_uppercase && !include_lowercase && !include_numbers && !include_symbols {
                self.string_result_entryrow.set_text("");
                return;
            }

            // Build character sets
            let uppercase_chars: Vec<char> = if avoid_ambiguous {
                ('A'..='Z')
                    .filter(|c| !['I', 'O', 'G'].contains(c))
                    .collect()
            } else {
                ('A'..='Z').collect()
            };

            let lowercase_chars: Vec<char> = if avoid_ambiguous {
                ('a'..='z')
                    .filter(|c| !['i', 'l', 'o'].contains(c))
                    .collect()
            } else {
                ('a'..='z').collect()
            };

            let number_chars: Vec<char> = if avoid_ambiguous {
                ('0'..='9')
                    .filter(|c| !['0', '1', '6'].contains(c))
                    .collect()
            } else {
                ('0'..='9').collect()
            };

            let symbol_chars: Vec<char> = "!@#$%^&*".chars().collect();
            let mut pool: Vec<char> = Vec::new();

            if include_uppercase {
                pool.extend_from_slice(&uppercase_chars);
            }
            if include_lowercase {
                pool.extend_from_slice(&lowercase_chars);
            }
            if include_numbers {
                pool.extend_from_slice(&number_chars);
            }
            if include_symbols {
                pool.extend_from_slice(&symbol_chars);
            }

            // Validate: minimum requirements don't exceed total length
            let required_min = (if include_numbers { min_numbers } else { 0 })
                + (if include_symbols { min_symbols } else { 0 });

            if required_min > length || pool.is_empty() {
                self.string_result_entryrow.set_text("");
                return;
            }

            // Random generation logic
            let mut rng = rand::thread_rng();
            let mut result = Vec::with_capacity(length);

            // Mins first
            if include_numbers {
                for _ in 0..min_numbers {
                    let ch = number_chars[rng.gen_range(0..number_chars.len())];
                    result.push(ch);
                }
            }
            if include_symbols {
                for _ in 0..min_symbols {
                    let ch = symbol_chars[rng.gen_range(0..symbol_chars.len())];
                    result.push(ch);
                }
            }

            // Fill rest
            let remaining_length = length - result.len();
            for _ in 0..remaining_length {
                let ch = pool[rng.gen_range(0..pool.len())];
                result.push(ch);
            }

            // Shuffle result to avoid predictable patterns
            result.shuffle(&mut rng);

            self.string_result_entryrow
                .set_text(&result.into_iter().collect::<String>());
        }

        fn update_number_result(&self) {
            let min = self.number_min_spinrow.value() as i64;
            let max = self.number_max_spinrow.value() as i64;

            if min > max {
                self.number_result_entryrow.set_text("");
                return;
            }

            let mut rng = rand::thread_rng();
            let result = rng.gen_range(min..=max);
            self.number_result_entryrow.set_text(&result.to_string());
        }

        fn update_passphrase_result(&self) {
            let length = self.passphrase_length_spinrow.value() as usize;
            let separator = self.passphrase_separator_entryrow.text();
            let capitalize = self.passphrase_capitalize_checkbutton.is_active();
            let include_number = self.passphrase_include_number_checkbutton.is_active();

            if length == 0 {
                self.passphrase_result_entryrow.set_text("");
                return;
            }

            let mut rng = rand::thread_rng();
            let mut words: Vec<String> = (0..length)
                .map(|_| {
                    let word = eff_wordlist::large::random_word().to_string();
                    if capitalize {
                        word[..1].to_uppercase() + &word[1..]
                    } else {
                        word
                    }
                })
                .collect();

            if include_number {
                let number: u32 = rng.gen_range(0..100);
                let index = rng.gen_range(0..words.len());

                if rng.gen_bool(0.5) {
                    words[index] = format!("{}{}", number, words[index]);
                } else {
                    words[index] = format!("{}{}", words[index], number);
                }
            }

            let result = words.join(&separator);
            self.passphrase_result_entryrow.set_text(&result);
        }
    }

    impl ObjectImpl for RandomWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.update_string_result();
            self.update_number_result();
            self.update_passphrase_result();
        }
    }

    impl WidgetImpl for RandomWidget {}
    impl BinImpl for RandomWidget {}
}

glib::wrapper! {
    pub struct RandomWidget(ObjectSubclass<imp::RandomWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl RandomWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
