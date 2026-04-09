/*
 * color_blindness.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, CompositeTemplate};

mod imp {
    use adw::prelude::ComboRowExt;
    use color_blinder::{Config, FilterKind, ProcessingStyle, RgbaBuf};
    use gettextrs::gettext;
    use gtk::gio;

    use crate::core::widgets::ImageArea;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/color_blindness/color_blindness.ui")]
    pub struct ColorBlindnessWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        filter_comborow: TemplateChild<adw::ComboRow>,

        #[template_child]
        original_imagearea: TemplateChild<ImageArea>,

        #[template_child]
        filtered_imagearea: TemplateChild<ImageArea>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for ColorBlindnessWidget {
        const NAME: &'static str = "ColorBlindnessWidget";
        type Type = super::ColorBlindnessWidget;
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
    impl ColorBlindnessWidget {
        fn show_error_toast(&self, message: impl Into<String>) {
            self.toast_overlay.dismiss_all();
            let toast = adw::Toast::builder().title(message.into()).build();
            self.toast_overlay.add_toast(toast);
        }

        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_selected_filter_comborow(&self) {
            self.do_filter_image();
        }

        #[template_callback]
        fn on_signal_image_loaded_original_imagearea(&self) {
            self.do_filter_image();
        }

        #[template_callback]
        fn on_signal_cleared_original_imagearea(&self) {
            self.filtered_imagearea.set_file(None::<gio::File>);
        }

        #[template_callback]
        fn on_signal_error_filtered_imagearea(&self, error_message: String) {
            self.show_error_toast(error_message);
        }

        #[template_callback]
        fn on_signal_view_requested_filtered_imagearea(&self) -> bool {
            false
        }

        #[template_callback]
        fn on_signal_image_saved_filtered_imagearea(&self, save_path: String) {
            // Store the saved file
            let file = gio::File::for_path(save_path.clone());

            // Show toast with "Open" button
            let obj = self.obj().clone();
            let toast = adw::Toast::builder()
                .title(gettext("Image saved"))
                .button_label("Open")
                .build();
            toast.connect_button_clicked(move |_| {
                let parent = obj.root().and_downcast::<gtk::Window>();
                let file = file.clone();
                glib::spawn_future_local(async move {
                    let launcher = gtk::FileLauncher::new(Some(&file));
                    launcher
                        .launch_future(parent.as_ref())
                        .await
                        .unwrap_or_else(|err| {
                            eprintln!("Failed to launch file: {}", err);
                        });
                });
            });
            self.toast_overlay.add_toast(toast);
        }

        // Other methods
        fn parse_filter(&self) -> color_blinder::FilterKind {
            let index = self.filter_comborow.selected();
            match index {
                0 => FilterKind::ACHROMATOMALY,
                1 => FilterKind::ACHROMATOPSIA,
                2 => FilterKind::DEUTERANOPIABVM97,
                3 => FilterKind::PROTANOPIABVM97,
                4 => FilterKind::TRITANOPIABVM97,
                _ => unreachable!("Invalid filter index {index}"),
            }
        }

        fn do_filter_image(&self) {
            let filter = self.parse_filter();

            let Some(original_image_file) = self.original_imagearea.file().path() else {
                self.show_error_toast("Unable to access the selected image file.");
                return;
            };

            let original_image_rgba = match image::open(&original_image_file) {
                Ok(img) => img.to_rgba8(),
                Err(err) => {
                    self.show_error_toast(format!(
                        "Unable to decode image: {} ({err})",
                        original_image_file.display()
                    ));
                    return;
                }
            };

            let (w, h) = original_image_rgba.dimensions();
            let Some(original_image_buf) = RgbaBuf::from_raw(w, h, original_image_rgba.into_raw())
            else {
                self.show_error_toast("Unable to build RGBA buffer for filtering.");
                return;
            };

            let context = Config {
                combine_output: false,
                processing: ProcessingStyle::Inline,
                render_label: false,
            }
            .into_context();

            let Ok(result) = context.process(original_image_buf, filter) else {
                self.show_error_toast("Color filtering failed.");
                return;
            };

            let Some((_label, out)) = result.into_iter().next() else {
                self.show_error_toast("Color filter returned no output image.");
                return;
            };

            let Ok((temp_file, _stream)) = gio::File::new_tmp(Some(&"devtoolbox_XXXXXX.png"))
            else {
                self.show_error_toast("Unable to create a temporary output file.");
                return;
            };

            let Some(temp_path) = temp_file.path() else {
                self.show_error_toast("Temporary output path is not a local filesystem path.");
                return;
            };

            if let Err(err) = out.save(&temp_path) {
                self.show_error_toast(format!("Unable to save filtered image: {err}"));
                return;
            }

            self.filtered_imagearea.set_file(Some(temp_file));
        }
    }

    impl ObjectImpl for ColorBlindnessWidget {}
    impl WidgetImpl for ColorBlindnessWidget {}
    impl BinImpl for ColorBlindnessWidget {}
}

glib::wrapper! {
    pub struct ColorBlindnessWidget(ObjectSubclass<imp::ColorBlindnessWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl ColorBlindnessWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
