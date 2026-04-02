/*
 * regex.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gio, glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

mod imp {
    use gtk::gdk;

    use crate::core::widgets::TextArea;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/devtoolbox/tools/regex/regex.ui")]
    #[properties(wrapper_type = super::RegexWidget)]
    pub struct RegexWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        regex_textarea: TemplateChild<TextArea>,

        #[template_child]
        textarea: TemplateChild<TextArea>,

        // Properties
        #[property(get, set, type = bool, default = false)]
        dragging: RefCell<bool>,

        #[property(get, set, type = bool, default = false)]
        working: RefCell<bool>,

        // Other fields
        tag: RefCell<gtk::TextTag>,
        match_job_id: RefCell<u64>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for RegexWidget {
        const NAME: &'static str = "RegexWidget";
        type Type = super::RegexWidget;
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
    impl RegexWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_changed_regex_textarea(&self) {
            self.do_matching();
        }

        #[template_callback]
        fn on_signal_error_regex_textarea(&self, error_message: String) {
            self.regex_textarea.set_error(true);
            self.regex_textarea.set_error_label(error_message);
        }

        #[template_callback]
        fn on_signal_cleared_regex_textarea(&self) {
            self.do_matching();
        }

        #[template_callback]
        fn on_signal_changed_textarea(&self) {
            self.do_matching();
        }

        #[template_callback]
        fn on_signal_error_textarea(&self, error_message: String) {
            self.textarea.set_error(true);
            self.textarea.set_error_label(error_message);
        }

        // Other methods
        fn do_matching(&self) {
            let pattern = self.regex_textarea.text();
            let text = self.textarea.text();

            let buffer = self.textarea.buffer();
            let tag = self.tag.borrow().clone();
            buffer.remove_tag(&tag, &buffer.start_iter(), &buffer.end_iter());

            self.regex_textarea.set_error(false);
            self.regex_textarea.set_error_label(String::new());

            if pattern.is_empty() || text.is_empty() {
                self.obj().set_working(false);
                return;
            }

            let job_id = {
                let mut id = self.match_job_id.borrow_mut();
                *id += 1;
                *id
            };

            self.obj().set_working(true);

            let obj = self.obj().downgrade();
            glib::spawn_future_local(async move {
                let result = gio::spawn_blocking(move || -> Result<Vec<(i32, i32)>, String> {
                    let regex = regex::Regex::new(&pattern).map_err(|e| e.to_string())?;
                    Ok(regex
                        .find_iter(&text)
                        .map(|m| (m.start() as i32, m.end() as i32))
                        .collect())
                })
                .await;

                let Some(obj) = obj.upgrade() else {
                    return;
                };
                let imp = obj.imp();

                if *imp.match_job_id.borrow() != job_id {
                    return;
                }

                let buffer = imp.textarea.buffer();
                let tag = imp.tag.borrow().clone();
                buffer.remove_tag(&tag, &buffer.start_iter(), &buffer.end_iter());

                match result {
                    Ok(Ok(ranges)) => {
                        imp.regex_textarea.set_error(false);
                        for (start, end) in ranges {
                            let start_iter = buffer.iter_at_offset(start);
                            let end_iter = buffer.iter_at_offset(end);
                            buffer.apply_tag(&tag, &start_iter, &end_iter);
                        }
                    }
                    Ok(Err(error_message)) => {
                        imp.regex_textarea.set_error(true);
                        imp.regex_textarea.set_error_label(error_message);
                    }
                    Err(_) => {
                        imp.regex_textarea.set_error(true);
                        imp.regex_textarea
                            .set_error_label("Regex matching task failed unexpectedly");
                    }
                }

                obj.set_working(false);
            });
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for RegexWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.obj()
                .bind_property("working", &*self.regex_textarea, "working")
                .build();
            self.obj()
                .bind_property("working", &*self.textarea, "working")
                .build();

            self.tag.replace(
                self.textarea
                    .buffer()
                    .create_tag(Some("match"), &[("background", &"#005eff7f")])
                    .unwrap(),
            );

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
        }
    }

    impl WidgetImpl for RegexWidget {}
    impl BinImpl for RegexWidget {}
}

glib::wrapper! {
    pub struct RegexWidget(ObjectSubclass<imp::RegexWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl RegexWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
