/*
 * contrast_check.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::{
    gdk, glib,
    prelude::{StyleContextExt, WidgetExt},
    CompositeTemplate, STYLE_PROVIDER_PRIORITY_APPLICATION,
};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/tools/contrast_check/contrast_check.ui")]
    pub struct ContrastCheckWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        swap_button: TemplateChild<gtk::Button>,

        #[template_child]
        fg_color_button: TemplateChild<gtk::ColorDialogButton>,

        #[template_child]
        bg_color_button: TemplateChild<gtk::ColorDialogButton>,

        #[template_child]
        example_box: TemplateChild<gtk::Box>,

        #[template_child]
        example_title: TemplateChild<gtk::Label>,

        #[template_child]
        example_text: TemplateChild<gtk::Label>,

        #[template_child]
        aa_small_image: TemplateChild<gtk::Image>,

        #[template_child]
        aa_large_image: TemplateChild<gtk::Image>,

        #[template_child]
        aaa_small_image: TemplateChild<gtk::Image>,

        #[template_child]
        aaa_large_image: TemplateChild<gtk::Image>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for ContrastCheckWidget {
        const NAME: &'static str = "ContrastCheckWidget";
        type Type = super::ContrastCheckWidget;
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
    impl ContrastCheckWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_clicked_swap_button(&self) {
            let fg_color = self.fg_color_button.rgba();
            let bg_color = self.bg_color_button.rgba();

            self.fg_color_button.set_rgba(&bg_color);
            self.bg_color_button.set_rgba(&fg_color);
        }

        #[template_callback]
        fn on_signal_notify_rgba_fg_color_button(&self) {
            self.set_example_box();
            self.check_wcag();
        }

        #[template_callback]
        fn on_signal_notify_rgba_bg_color_button(&self) {
            self.set_example_box();
            self.check_wcag();
        }

        // Other methods
        fn set_example_box(&self) {
            let fg_color = self.fg_color_button.rgba();
            let bg_color = self.bg_color_button.rgba();

            let fg_css_str = format!("* {{ color: {fg_color}; }}");
            let bg_css_str = format!("* {{ background-color: {bg_color};}} ");

            let fg_css_provider = gtk::CssProvider::new();
            let bg_css_provider = gtk::CssProvider::new();

            fg_css_provider.load_from_string(&fg_css_str);
            bg_css_provider.load_from_string(&bg_css_str);

            // Deprecation warning is relative to GTK 5, where style contexts will
            // get removed.
            self.example_title
                .style_context()
                .add_provider(&fg_css_provider, STYLE_PROVIDER_PRIORITY_APPLICATION);
            self.example_text
                .style_context()
                .add_provider(&fg_css_provider, STYLE_PROVIDER_PRIORITY_APPLICATION);
            self.example_box
                .style_context()
                .add_provider(&bg_css_provider, STYLE_PROVIDER_PRIORITY_APPLICATION);
        }

        fn check_wcag(&self) {
            let fg_luminance = self.compute_luminance(&self.fg_color_button.rgba());
            let bg_luminance = self.compute_luminance(&self.bg_color_button.rgba());

            let ratio = if fg_luminance > bg_luminance {
                (fg_luminance + 0.05) / (bg_luminance + 0.05)
            } else {
                (bg_luminance + 0.05) / (fg_luminance + 0.05)
            };

            let aa_large = ratio >= 3.0;
            let aa_small = ratio >= 4.5;
            let aaa_large = ratio >= 4.5;
            let aaa_small = ratio >= 7.0;

            if aa_large {
                self.aa_large_image
                    .set_icon_name(Some("check-round-outline2"));
                self.aa_large_image.remove_css_class("error");
                self.aa_large_image.add_css_class("success");
            } else {
                self.aa_large_image
                    .set_icon_name(Some("minus-circle-outline"));
                self.aa_large_image.remove_css_class("success");
                self.aa_large_image.add_css_class("error");
            }

            if aa_small {
                self.aa_small_image
                    .set_icon_name(Some("check-round-outline2"));
                self.aa_small_image.remove_css_class("error");
                self.aa_small_image.add_css_class("success");
            } else {
                self.aa_small_image
                    .set_icon_name(Some("minus-circle-outline"));
                self.aa_small_image.remove_css_class("success");
                self.aa_small_image.add_css_class("error");
            }

            if aaa_large {
                self.aaa_large_image
                    .set_icon_name(Some("check-round-outline2"));
                self.aaa_large_image.remove_css_class("error");
                self.aaa_large_image.add_css_class("success");
            } else {
                self.aaa_large_image
                    .set_icon_name(Some("minus-circle-outline"));
                self.aaa_large_image.remove_css_class("success");
                self.aaa_large_image.add_css_class("error");
            }

            if aaa_small {
                self.aaa_small_image
                    .set_icon_name(Some("check-round-outline2"));
                self.aaa_small_image.remove_css_class("error");
                self.aaa_small_image.add_css_class("success");
            } else {
                self.aaa_small_image
                    .set_icon_name(Some("minus-circle-outline"));
                self.aaa_small_image.remove_css_class("success");
                self.aaa_small_image.add_css_class("error");
            }
        }

        fn compute_luminance(&self, rgba: &gdk::RGBA) -> f64 {
            let r = self.luminance(rgba.red() as f64);
            let g = self.luminance(rgba.green() as f64);
            let b = self.luminance(rgba.blue() as f64);

            0.2126 * r + 0.7152 * g + 0.0722 * b
        }

        fn luminance(&self, value: f64) -> f64 {
            if value <= 0.03928 {
                value / 12.92
            } else {
                ((value + 0.055) / 1.055).powf(2.4)
            }
        }
    }

    impl ObjectImpl for ContrastCheckWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.set_example_box();
            self.check_wcag();
        }
    }

    impl WidgetImpl for ContrastCheckWidget {}
    impl BinImpl for ContrastCheckWidget {}
}

glib::wrapper! {
    pub struct ContrastCheckWidget(ObjectSubclass<imp::ContrastCheckWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl ContrastCheckWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
