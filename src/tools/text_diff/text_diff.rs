/*
 * text_diff.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gio, glib, CompositeTemplate};

use std::cell::RefCell;

mod imp {
    use crate::{
        core::widgets::TextArea,
        tools::text_diff::diff::{self, HighlightType},
    };

    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/text_diff/text_diff.ui")]
    pub struct TextDiffWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        old_textarea: TemplateChild<TextArea>,

        #[template_child]
        new_textarea: TemplateChild<TextArea>,

        #[template_child]
        diff_textarea: TemplateChild<TextArea>,

        // Other fields
        tag_removed_line: RefCell<Option<gtk::TextTag>>,
        tag_added_line: RefCell<Option<gtk::TextTag>>,
        tag_removed: RefCell<Option<gtk::TextTag>>,
        tag_added: RefCell<Option<gtk::TextTag>>,
        diff_job_id: RefCell<u64>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for TextDiffWidget {
        const NAME: &'static str = "TextDiffWidget";
        type Type = super::TextDiffWidget;
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
    impl TextDiffWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_changed_old_textarea(&self) {
            self.do_diff();
        }

        #[template_callback]
        fn on_signal_error_old_textarea(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }

        #[template_callback]
        fn on_signal_changed_new_textarea(&self) {
            self.do_diff();
        }

        #[template_callback]
        fn on_signal_error_new_textarea(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }

        // Other methods
        fn do_diff(&self) {
            let old_text = self.old_textarea.text();
            let new_text = self.new_textarea.text();

            // Bail out if either textarea is empty
            if old_text.is_empty() || new_text.is_empty() {
                self.diff_textarea.set_text(String::new());
                self.diff_textarea.set_working(false);
                return;
            }

            // Clear old diff results
            let buffer = self.diff_textarea.buffer();
            let start_iter = buffer.start_iter();
            let end_iter = buffer.end_iter();
            buffer.remove_tag_by_name("removed-line", &start_iter, &end_iter);
            buffer.remove_tag_by_name("added-line", &start_iter, &end_iter);
            buffer.remove_tag_by_name("removed", &start_iter, &end_iter);
            buffer.remove_tag_by_name("added", &start_iter, &end_iter);

            // Compute diff
            self.diff_textarea.set_working(true);

            let job_id = {
                let mut id = self.diff_job_id.borrow_mut();
                *id += 1;
                *id
            };

            let obj = self.obj().downgrade();
            glib::spawn_future_local(async move {
                let result =
                    gio::spawn_blocking(move || diff::compute_diff(&old_text, &new_text)).await;

                let Some(obj) = obj.upgrade() else {
                    return;
                };
                let imp = obj.imp();

                if *imp.diff_job_id.borrow() != job_id {
                    return;
                }

                match result {
                    Ok(Ok((output_text, highlights))) => {
                        imp.diff_textarea.set_text(output_text);
                        let buffer = imp.diff_textarea.buffer();

                        // Re-clear tags on the fresh buffer contents.
                        let start_iter = buffer.start_iter();
                        let end_iter = buffer.end_iter();
                        buffer.remove_tag_by_name("removed-line", &start_iter, &end_iter);
                        buffer.remove_tag_by_name("added-line", &start_iter, &end_iter);
                        buffer.remove_tag_by_name("removed", &start_iter, &end_iter);
                        buffer.remove_tag_by_name("added", &start_iter, &end_iter);

                        for (tag_type, start, end) in highlights {
                            let tag = match tag_type {
                                HighlightType::RemovedLine => imp.tag_removed_line.borrow().clone(),
                                HighlightType::AddedLine => imp.tag_added_line.borrow().clone(),
                                HighlightType::Removed => imp.tag_removed.borrow().clone(),
                                HighlightType::Added => imp.tag_added.borrow().clone(),
                            };

                            if let Some(tag) = tag {
                                let start_iter = buffer.iter_at_offset(start as i32);
                                let end_iter = buffer.iter_at_offset(end as i32);
                                buffer.apply_tag(&tag, &start_iter, &end_iter);
                            }
                        }
                    }
                    Ok(Err(error_message)) => {
                        imp.toast_overlay
                            .add_toast(adw::Toast::builder().title(error_message).build());
                    }
                    Err(_) => {
                        imp.toast_overlay.add_toast(
                            adw::Toast::builder()
                                .title("An unexpected error occurred while computing the diff.")
                                .build(),
                        );
                    }
                }

                imp.diff_textarea.set_working(false);
            });
        }
    }

    impl ObjectImpl for TextDiffWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Initialize text tags
            let style_manager = adw::StyleManager::default();
            let is_current_dark = style_manager.is_dark();
            self.tag_removed_line.replace(Some(
                gtk::TextTag::builder()
                    .name("removed-line")
                    .background(if is_current_dark {
                        "#5d2a2a"
                    } else {
                        "#f2b8b8"
                    })
                    .build(),
            ));
            self.diff_textarea
                .buffer()
                .tag_table()
                .add(self.tag_removed_line.borrow().as_ref().unwrap());
            self.tag_added_line.replace(Some(
                gtk::TextTag::builder()
                    .name("added-line")
                    .background(if is_current_dark {
                        "#494f3b"
                    } else {
                        "#d9e6c3"
                    })
                    .build(),
            ));
            self.diff_textarea
                .buffer()
                .tag_table()
                .add(self.tag_added_line.borrow().as_ref().unwrap());
            self.tag_removed.replace(Some(
                gtk::TextTag::builder()
                    .name("removed")
                    .background(if is_current_dark {
                        "#7d2121"
                    } else {
                        "#d07a7a"
                    })
                    .build(),
            ));
            self.diff_textarea
                .buffer()
                .tag_table()
                .add(self.tag_removed.borrow().as_ref().unwrap());
            self.tag_added.replace(Some(
                gtk::TextTag::builder()
                    .name("added")
                    .background(if is_current_dark {
                        "#5b7822"
                    } else {
                        "#a8c65f"
                    })
                    .build(),
            ));
            self.diff_textarea
                .buffer()
                .tag_table()
                .add(self.tag_added.borrow().as_ref().unwrap());

            // Connect to style changes to update text tags colors
            let obj = self.obj().clone();
            style_manager.connect_dark_notify(move |_| {
                let style_manager = adw::StyleManager::default();
                let is_current_dark = style_manager.is_dark();
                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .remove(obj.imp().tag_removed_line.borrow().as_ref().unwrap());
                obj.imp().tag_removed_line.replace(Some(
                    gtk::TextTag::builder()
                        .name("removed-line")
                        .background(if is_current_dark {
                            "#5d2a2a"
                        } else {
                            "#f2b8b8"
                        })
                        .build(),
                ));
                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .add(obj.imp().tag_removed_line.borrow().as_ref().unwrap());

                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .remove(obj.imp().tag_added_line.borrow().as_ref().unwrap());
                obj.imp().tag_added_line.replace(Some(
                    gtk::TextTag::builder()
                        .name("added-line")
                        .background(if is_current_dark {
                            "#494f3b"
                        } else {
                            "#d9e6c3"
                        })
                        .build(),
                ));
                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .add(obj.imp().tag_added_line.borrow().as_ref().unwrap());

                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .remove(obj.imp().tag_removed.borrow().as_ref().unwrap());
                obj.imp().tag_removed.replace(Some(
                    gtk::TextTag::builder()
                        .name("removed")
                        .background(if is_current_dark {
                            "#7d2121"
                        } else {
                            "#d07a7a"
                        })
                        .build(),
                ));
                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .add(obj.imp().tag_removed.borrow().as_ref().unwrap());

                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .remove(obj.imp().tag_added.borrow().as_ref().unwrap());
                obj.imp().tag_added.replace(Some(
                    gtk::TextTag::builder()
                        .name("added")
                        .background(if is_current_dark {
                            "#5b7822"
                        } else {
                            "#a8c65f"
                        })
                        .build(),
                ));
                obj.imp()
                    .diff_textarea
                    .buffer()
                    .tag_table()
                    .add(obj.imp().tag_added.borrow().as_ref().unwrap());

                obj.imp().do_diff();
            });
        }
    }

    impl WidgetImpl for TextDiffWidget {}
    impl BinImpl for TextDiffWidget {}
}

glib::wrapper! {
    pub struct TextDiffWidget(ObjectSubclass<imp::TextDiffWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl TextDiffWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
