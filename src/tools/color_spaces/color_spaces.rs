/*
 * color_spaces.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::core::widgets::ActionableEntryRow;
use crate::tools::color_spaces::color_conversion::*;
use crate::{connect_imp_signal, connect_imp_signals};
use adw::subclass::prelude::*;
use gtk::{gdk, glib, glib::Properties, CompositeTemplate};
use std::cell::RefCell;

use adw::prelude::ComboRowExt;
use gtk::prelude::{EditableExt, WidgetExt};
use sourceview::prelude::ObjectExt;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/devtoolbox/tools/color_spaces/color_spaces.ui")]
    #[properties(wrapper_type = super::ColorSpacesWidget)]
    pub struct ColorSpacesWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        output_format_comborow: TemplateChild<adw::ComboRow>,

        #[template_child]
        angle_unit_comborow: TemplateChild<adw::ComboRow>,

        #[template_child]
        precision_bits_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        color_button: TemplateChild<gtk::ColorDialogButton>,

        #[template_child]
        hex_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        rgb_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hsl_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hwb_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        rgb_red_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        rgb_green_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        rgb_blue_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hsv_hue_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hsv_saturation_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hsv_value_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hsl_hue_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hsl_saturation_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        hsl_lightness_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        alpha_entryrow: TemplateChild<ActionableEntryRow>,

        // State
        current_color: RefCell<Color>,

        // Signal handlers
        color_button_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hex_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        rgb_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hsl_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hwb_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        rgb_red_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        rgb_green_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        rgb_blue_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hsv_hue_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hsv_saturation_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hsv_value_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hsl_hue_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hsl_saturation_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        hsl_lightness_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
        alpha_entryrow_signal_handler_id: RefCell<Option<glib::SignalHandlerId>>,
    }

    // impl Default for ColorSpacesWidget {
    //     fn default() -> Self {
    //         Self {
    //             current_color: RefCell::new(Color::new(0.0706, 0.3294, 0.6510, 1.0)),
    //             ..Default::default()
    //         }
    //     }
    // }

    #[glib::object_subclass]
    impl ObjectSubclass for ColorSpacesWidget {
        const NAME: &'static str = "ColorSpacesWidget";
        type Type = super::ColorSpacesWidget;
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
    impl ColorSpacesWidget {
        // Closures
        #[template_callback]
        fn is_web_format_selected_closure(&self, selected_format: u32) -> bool {
            matches!(selected_format, 0)
        }

        #[template_callback]
        fn is_web_format_not_selected_closure(&self, selected_format: u32) -> bool {
            !matches!(selected_format, 0)
        }

        #[template_callback]
        fn is_precision_bits_spinrow_visible_closure(&self, selected_format: u32) -> bool {
            matches!(selected_format, 3)
        }

        // Template callbacks
        #[template_callback]
        fn on_signal_notify_selected_output_format_comborow(&self) {
            self.update_all_displays();
        }

        #[template_callback]
        fn on_signal_notify_selected_angle_unit_comborow(&self) {
            let color = *self.current_color.borrow();
            let (hue, _, _) = rgb_to_hsl(&color);

            self.hsv_hue_entryrow.block_signal(
                self.hsv_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsl_hue_entryrow.block_signal(
                self.hsl_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );

            self.hsv_hue_entryrow.set_text(&self.format_angle(hue));
            self.hsl_hue_entryrow.set_text(&self.format_angle(hue));

            self.hsv_hue_entryrow.unblock_signal(
                self.hsv_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsl_hue_entryrow.unblock_signal(
                self.hsl_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        #[template_callback]
        fn on_signal_notify_value_precision_bits_spinrow(&self) {
            self.update_all_displays();
        }

        #[template_callback]
        fn on_signal_notify_rgba_color_button(&self) {
            let rgba = self.color_button.rgba();
            *self.current_color.borrow_mut() =
                Color::new(rgba.red(), rgba.green(), rgba.blue(), rgba.alpha());
            self.update_all_displays();
        }

        #[template_callback]
        fn on_signal_changed_hex_entryrow(&self) {
            let text = self.hex_entryrow.text().to_string();
            if let Some(color) = parse_css_color(&text) {
                *self.current_color.borrow_mut() = color;
                self.hex_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hex"]);
            } else {
                self.hex_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_rgb_entryrow(&self) {
            let text = self.rgb_entryrow.text().to_string();
            if let Some(color) = parse_css_color(&text) {
                *self.current_color.borrow_mut() = color;
                self.rgb_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["rgb"]);
            } else {
                self.rgb_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hsl_entryrow(&self) {
            let text = self.hsl_entryrow.text().to_string();
            if let Some(color) = parse_css_color(&text) {
                *self.current_color.borrow_mut() = color;
                self.hsl_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hsl"]);
            } else {
                self.hsl_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hwb_entryrow(&self) {
            let text = self.hwb_entryrow.text().to_string();
            if let Some(color) = parse_css_color(&text) {
                *self.current_color.borrow_mut() = color;
                self.hwb_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hwb"]);
            } else {
                self.hwb_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_rgb_red_entryrow(&self) {
            if let Ok(value) = self.parse_number(&self.rgb_red_entryrow.text()) {
                let mut color = self.current_color.borrow_mut();
                color.red = value;
                self.rgb_red_entryrow.remove_css_class("error");
                drop(color);
                self.update_all_displays_except(&["rgb"]);
            } else {
                self.rgb_red_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_rgb_green_entryrow(&self) {
            if let Ok(value) = self.parse_number(&self.rgb_green_entryrow.text()) {
                let mut color = self.current_color.borrow_mut();
                color.green = value;
                self.rgb_green_entryrow.remove_css_class("error");
                drop(color);
                self.update_all_displays_except(&["rgb"]);
            } else {
                self.rgb_green_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_rgb_blue_entryrow(&self) {
            if let Ok(value) = self.parse_number(&self.rgb_blue_entryrow.text()) {
                let mut color = self.current_color.borrow_mut();
                color.blue = value;
                self.rgb_blue_entryrow.remove_css_class("error");
                drop(color);
                self.update_all_displays_except(&["rgb"]);
            } else {
                self.rgb_blue_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hsv_hue_entryrow(&self) {
            if let Ok(h) = self.parse_angle(&self.hsv_hue_entryrow.text()) {
                let color = self.current_color.borrow();
                let (_, s, v) = rgb_to_hsv(&color);
                let new_color = hsv_to_rgb(h, s, v, color.alpha);
                drop(color);
                *self.current_color.borrow_mut() = new_color;
                self.hsv_hue_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hsv"]);
            } else {
                self.hsv_hue_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hsv_saturation_entryrow(&self) {
            if let Ok(s) = self.parse_number(&self.hsv_saturation_entryrow.text()) {
                let color = self.current_color.borrow();
                let (h, _, v) = rgb_to_hsv(&color);
                let new_color = hsv_to_rgb(h, s, v, color.alpha);
                drop(color);
                *self.current_color.borrow_mut() = new_color;
                self.hsv_saturation_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hsv"]);
            } else {
                self.hsv_saturation_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hsv_value_entryrow(&self) {
            if let Ok(v) = self.parse_number(&self.hsv_value_entryrow.text()) {
                let color = self.current_color.borrow();
                let (h, s, _) = rgb_to_hsv(&color);
                let new_color = hsv_to_rgb(h, s, v, color.alpha);
                drop(color);
                *self.current_color.borrow_mut() = new_color;
                self.hsv_value_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hsv"]);
            } else {
                self.hsv_value_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hsl_hue_entryrow(&self) {
            if let Ok(h) = self.parse_angle(&self.hsl_hue_entryrow.text()) {
                let color = self.current_color.borrow();
                let (_, s, l) = rgb_to_hsl(&color);
                let new_color = hsl_to_rgb(h, s, l, color.alpha);
                drop(color);
                *self.current_color.borrow_mut() = new_color;
                self.hsl_hue_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hsl"]);
            } else {
                self.hsl_hue_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hsl_saturation_entryrow(&self) {
            if let Ok(s) = self.parse_number(&self.hsl_saturation_entryrow.text()) {
                let color = self.current_color.borrow();
                let (h, _, l) = rgb_to_hsl(&color);
                let new_color = hsl_to_rgb(h, s, l, color.alpha);
                drop(color);
                *self.current_color.borrow_mut() = new_color;
                self.hsl_saturation_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hsl"]);
            } else {
                self.hsl_saturation_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_hsl_lightness_entryrow(&self) {
            if let Ok(l) = self.parse_number(&self.hsl_lightness_entryrow.text()) {
                let color = self.current_color.borrow();
                let (h, s, _) = rgb_to_hsl(&color);
                let new_color = hsl_to_rgb(h, s, l, color.alpha);
                drop(color);
                *self.current_color.borrow_mut() = new_color;
                self.hsl_lightness_entryrow.remove_css_class("error");
                self.update_all_displays_except(&["hsl"]);
            } else {
                self.hsl_lightness_entryrow.add_css_class("error");
            }
        }

        #[template_callback]
        fn on_signal_changed_alpha_entryrow(&self) {
            if let Ok(alpha) = self.parse_number(&self.alpha_entryrow.text()) {
                let mut color = self.current_color.borrow_mut();
                color.alpha = alpha;
                self.alpha_entryrow.remove_css_class("error");
                drop(color);
                self.update_all_displays_except(&["alpha"]);
            } else {
                self.alpha_entryrow.add_css_class("error");
            }
        }

        // Other methods
        fn update_all_displays(&self) {
            self.update_all_displays_except(&[]);
        }

        fn update_all_displays_except(&self, exclude: &[&str]) {
            if !exclude.contains(&"color") {
                self.update_color_button();
            }
            if !exclude.contains(&"hex") {
                self.update_hex();
            }
            if !exclude.contains(&"rgb") {
                self.update_rgb();
            }
            if !exclude.contains(&"hsv") {
                self.update_hsv();
            }
            if !exclude.contains(&"hsl") {
                self.update_hsl();
            }
            if !exclude.contains(&"hwb") {
                self.update_hwb();
            }
            if !exclude.contains(&"alpha") {
                self.update_alpha();
            }
        }

        fn update_color_button(&self) {
            let color = *self.current_color.borrow();
            let gdk_rgba = gdk::RGBA::new(color.red, color.green, color.blue, color.alpha);

            self.color_button.block_signal(
                self.color_button_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.color_button.set_rgba(&gdk_rgba);
            self.color_button.unblock_signal(
                self.color_button_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        fn update_hex(&self) {
            let color = *self.current_color.borrow();
            let hex = color_to_hex(color);

            self.hex_entryrow.block_signal(
                self.hex_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hex_entryrow.set_text(&hex);
            self.hex_entryrow.remove_css_class("error");
            self.hex_entryrow.unblock_signal(
                self.hex_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        fn update_rgb(&self) {
            let color = *self.current_color.borrow();

            self.rgb_entryrow.block_signal(
                self.rgb_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.rgb_entryrow
                .set_text(&color_to_css_web_rgb_percentage(&color));
            self.rgb_entryrow.remove_css_class("error");
            self.rgb_entryrow.unblock_signal(
                self.rgb_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );

            self.rgb_red_entryrow.block_signal(
                self.rgb_red_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.rgb_green_entryrow.block_signal(
                self.rgb_green_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.rgb_blue_entryrow.block_signal(
                self.rgb_blue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );

            self.rgb_red_entryrow
                .set_text(&self.format_value(color.red));
            self.rgb_green_entryrow
                .set_text(&self.format_value(color.green));
            self.rgb_blue_entryrow
                .set_text(&self.format_value(color.blue));

            self.rgb_red_entryrow.remove_css_class("error");
            self.rgb_green_entryrow.remove_css_class("error");
            self.rgb_blue_entryrow.remove_css_class("error");

            self.rgb_red_entryrow.unblock_signal(
                self.rgb_red_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.rgb_green_entryrow.unblock_signal(
                self.rgb_green_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.rgb_blue_entryrow.unblock_signal(
                self.rgb_blue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        fn update_hsv(&self) {
            let color = *self.current_color.borrow();
            let (h, s, v) = rgb_to_hsv(&color);

            self.hsv_hue_entryrow.block_signal(
                self.hsv_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsv_saturation_entryrow.block_signal(
                self.hsv_saturation_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsv_value_entryrow.block_signal(
                self.hsv_value_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );

            self.hsv_hue_entryrow.set_text(&self.format_angle(h));
            self.hsv_saturation_entryrow.set_text(&self.format_value(s));
            self.hsv_value_entryrow.set_text(&self.format_value(v));

            self.hsv_hue_entryrow.remove_css_class("error");
            self.hsv_saturation_entryrow.remove_css_class("error");
            self.hsv_value_entryrow.remove_css_class("error");

            self.hsv_hue_entryrow.unblock_signal(
                self.hsv_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsv_saturation_entryrow.unblock_signal(
                self.hsv_saturation_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsv_value_entryrow.unblock_signal(
                self.hsv_value_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        fn update_hsl(&self) {
            let color = *self.current_color.borrow();
            let (h, s, l) = rgb_to_hsl(&color);

            self.hsl_entryrow.block_signal(
                self.hsl_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsl_entryrow.set_text(&color_to_css_hsl(&color));
            self.hsl_entryrow.remove_css_class("error");
            self.hsl_entryrow.unblock_signal(
                self.hsl_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );

            self.hsl_hue_entryrow.block_signal(
                self.hsl_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsl_saturation_entryrow.block_signal(
                self.hsl_saturation_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsl_lightness_entryrow.block_signal(
                self.hsl_lightness_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );

            self.hsl_hue_entryrow.set_text(&self.format_angle(h));
            self.hsl_saturation_entryrow.set_text(&self.format_value(s));
            self.hsl_lightness_entryrow.set_text(&self.format_value(l));

            self.hsl_hue_entryrow.remove_css_class("error");
            self.hsl_saturation_entryrow.remove_css_class("error");
            self.hsl_lightness_entryrow.remove_css_class("error");

            self.hsl_hue_entryrow.unblock_signal(
                self.hsl_hue_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsl_saturation_entryrow.unblock_signal(
                self.hsl_saturation_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hsl_lightness_entryrow.unblock_signal(
                self.hsl_lightness_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        fn update_hwb(&self) {
            let color = *self.current_color.borrow();

            self.hwb_entryrow.block_signal(
                self.hwb_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.hwb_entryrow.set_text(&color_to_css_hwb(&color));
            self.hwb_entryrow.remove_css_class("error");
            self.hwb_entryrow.unblock_signal(
                self.hwb_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        fn update_alpha(&self) {
            let color = *self.current_color.borrow();

            let alpha_text = if self.output_format_comborow.selected() == 2 {
                let s = format_decimal(color.alpha, 4);
                s.trim_end_matches('0').trim_end_matches('.').to_string()
            } else {
                self.format_value(color.alpha)
            };

            self.alpha_entryrow.block_signal(
                self.alpha_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
            self.alpha_entryrow.set_text(&alpha_text);
            self.alpha_entryrow.remove_css_class("error");
            self.alpha_entryrow.unblock_signal(
                self.alpha_entryrow_signal_handler_id
                    .borrow()
                    .as_ref()
                    .unwrap(),
            );
        }

        fn parse_number(&self, text: &str) -> Result<f32, String> {
            let format = self.output_format_comborow.selected();

            match format {
                3 => {
                    let bits = self.precision_bits_spinrow.value() as u32;
                    let value: u32 = text
                        .trim()
                        .parse()
                        .map_err(|_| "invalid integer value".to_string())?;

                    // guard against invalid bit width and out-of-range input
                    let max = if bits >= 32 {
                        u32::MAX
                    } else {
                        (1u32 << bits) - 1
                    };

                    if value > max {
                        return Err(format!("value out of range (0..={max})"));
                    }

                    Ok((value as f32) / (max as f32))
                }
                1 => {
                    let value: f32 = text
                        .trim()
                        .parse()
                        .map_err(|_| "invalid percentage value".to_string())?;

                    if !(0.0..=100.0).contains(&value) {
                        return Err("value out of range (0..=100)".to_string());
                    }

                    Ok(value / 100.0)
                }
                _ => {
                    let value: f32 = text
                        .trim()
                        .parse()
                        .map_err(|_| "invalid float value".to_string())?;

                    if !(0.0..=1.0).contains(&value) {
                        return Err("value out of range (0..=1)".to_string());
                    }

                    Ok(value)
                }
            }
        }

        fn parse_angle(&self, text: &str) -> Result<f32, String> {
            let angle_unit = self.angle_unit_comborow.selected();
            let value: f32 = text
                .trim()
                .parse()
                .map_err(|_| "invalid angle value".to_string())?;

            match angle_unit {
                0 => Ok(deg_to_normalized(value)),  // Degrees
                1 => Ok(rad_to_normalized(value)),  // Radians
                2 => Ok(grad_to_normalized(value)), // Gradians
                3 => Ok(value.clamp(0.0, 1.0)),     // Turns
                _ => self.parse_number(text),       // Follow format
            }
        }

        fn format_value(&self, value: f32) -> String {
            let format = self.output_format_comborow.selected();
            match format {
                3 => {
                    let bits = self.precision_bits_spinrow.value() as u32;
                    format!("{}", normalized_to_uintn(value, bits))
                }
                1 => format_decimal(normalized_to_percentage(value), 2),
                _ => format_decimal(value, 4),
            }
        }

        fn format_angle(&self, angle: f32) -> String {
            let angle_unit = self.angle_unit_comborow.selected();

            match angle_unit {
                0 => format_decimal(normalized_to_deg(angle), 2), // Degrees
                1 => format_decimal(normalized_to_rad(angle), 3), // Radians
                2 => format_decimal(normalized_to_grad(angle), 2), // Gradians
                3 => format_decimal(angle, 4),                    // Turns
                _ => self.format_value(angle),                    // Follow format
            }
        }
    }

    impl ObjectImpl for ColorSpacesWidget {
        fn constructed(&self) {
            self.parent_constructed();

            self.current_color
                .replace(Color::new(0.0706, 0.3294, 0.6510, 1.0));

            // Connect signals
            connect_imp_signals!(self;
                color_button_signal_handler_id <= color_button, "notify::rgba" => on_signal_notify_rgba_color_button;
                hex_entryrow_signal_handler_id <= hex_entryrow, "changed" => on_signal_changed_hex_entryrow;
                rgb_entryrow_signal_handler_id <= rgb_entryrow, "changed" => on_signal_changed_rgb_entryrow;
                hsl_entryrow_signal_handler_id <= hsl_entryrow, "changed" => on_signal_changed_hsl_entryrow;
                hwb_entryrow_signal_handler_id <= hwb_entryrow, "changed" => on_signal_changed_hwb_entryrow;
                rgb_red_entryrow_signal_handler_id <= rgb_red_entryrow, "changed" => on_signal_changed_rgb_red_entryrow;
                rgb_green_entryrow_signal_handler_id <= rgb_green_entryrow, "changed" => on_signal_changed_rgb_green_entryrow;
                rgb_blue_entryrow_signal_handler_id <= rgb_blue_entryrow, "changed" => on_signal_changed_rgb_blue_entryrow;
                hsv_hue_entryrow_signal_handler_id <= hsv_hue_entryrow, "changed" => on_signal_changed_hsv_hue_entryrow;
                hsv_saturation_entryrow_signal_handler_id <= hsv_saturation_entryrow, "changed" => on_signal_changed_hsv_saturation_entryrow;
                hsv_value_entryrow_signal_handler_id <= hsv_value_entryrow, "changed" => on_signal_changed_hsv_value_entryrow;
                hsl_hue_entryrow_signal_handler_id <= hsl_hue_entryrow, "changed" => on_signal_changed_hsl_hue_entryrow;
                hsl_saturation_entryrow_signal_handler_id <= hsl_saturation_entryrow, "changed" => on_signal_changed_hsl_saturation_entryrow;
                hsl_lightness_entryrow_signal_handler_id <= hsl_lightness_entryrow, "changed" => on_signal_changed_hsl_lightness_entryrow;
                alpha_entryrow_signal_handler_id <= alpha_entryrow, "changed" => on_signal_changed_alpha_entryrow;
            );

            self.update_all_displays();
        }
    }

    impl WidgetImpl for ColorSpacesWidget {}
    impl BinImpl for ColorSpacesWidget {}
}

glib::wrapper! {
    pub struct ColorSpacesWidget(ObjectSubclass<imp::ColorSpacesWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl ColorSpacesWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
