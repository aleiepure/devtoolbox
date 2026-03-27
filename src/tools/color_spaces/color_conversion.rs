/*
 * color_convertion.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use csscolorparser::Color as CssColor;
use palette::{convert::IntoColorUnclamped, Hsl, Hsv, Srgb};

#[derive(Default, Debug, Clone, Copy)]
pub struct Color {
    pub red: f32,
    pub green: f32,
    pub blue: f32,
    pub alpha: f32,
}

impl Color {
    pub fn new(red: f32, green: f32, blue: f32, alpha: f32) -> Self {
        Self {
            red: red.clamp(0.0, 1.0),
            green: green.clamp(0.0, 1.0),
            blue: blue.clamp(0.0, 1.0),
            alpha: alpha.clamp(0.0, 1.0),
        }
    }

    pub fn to_rgb_srgb(&self) -> Srgb {
        Srgb::new(self.red, self.green, self.blue)
    }

    pub fn from_rgb_srgb(srgb: &Srgb, alpha: f32) -> Self {
        Self::new(srgb.red, srgb.green, srgb.blue, alpha)
    }
}

// RGB to HSV
pub fn rgb_to_hsv(color: &Color) -> (f32, f32, f32) {
    let hsv: Hsv = color.to_rgb_srgb().into_color_unclamped();
    (
        hsv.hue.into_positive_degrees() / 360.0,
        hsv.saturation,
        hsv.value,
    )
}

// HSV to RGB
pub fn hsv_to_rgb(hue: f32, saturation: f32, value: f32, alpha: f32) -> Color {
    let hsv = Hsv::new(hue * 360.0, saturation, value);
    let srgb: Srgb = hsv.into_color_unclamped();
    Color::from_rgb_srgb(&srgb, alpha)
}

// RGB to HSL
pub fn rgb_to_hsl(color: &Color) -> (f32, f32, f32) {
    let hsl: Hsl = color.to_rgb_srgb().into_color_unclamped();
    (
        hsl.hue.into_positive_degrees() / 360.0,
        hsl.saturation,
        hsl.lightness,
    )
}

// HSL to RGB
pub fn hsl_to_rgb(hue: f32, saturation: f32, lightness: f32, alpha: f32) -> Color {
    let hsl = Hsl::new(hue * 360.0, saturation, lightness);
    let srgb: Srgb = hsl.into_color_unclamped();
    Color::from_rgb_srgb(&srgb, alpha)
}

// Noramalization functions
pub fn normalized_to_uint8(value: f32) -> u8 {
    (value.clamp(0.0, 1.0) * 255.0).round() as u8
}

pub fn uint8_to_normalized(value: u8) -> f32 {
    (value as f32) / 255.0
}

pub fn normalized_to_percentage(value: f32) -> f32 {
    value.clamp(0.0, 1.0) * 100.0
}

pub fn percentage_to_normalized(value: f32) -> f32 {
    (value / 100.0).clamp(0.0, 1.0)
}

pub fn normalized_to_uintn(value: f32, bits: u32) -> u32 {
    let max = (1u32 << bits) - 1;
    ((value.clamp(0.0, 1.0) * (max as f32)).round()) as u32
}

pub fn uintn_to_normalized(value: u32, bits: u32) -> f32 {
    let max = ((1u32 << bits) - 1) as f32;
    ((value as f32) / max).clamp(0.0, 1.0)
}

// Angle conversions
pub fn normalized_to_deg(value: f32) -> f32 {
    value.clamp(0.0, 1.0) * 360.0
}

pub fn deg_to_normalized(value: f32) -> f32 {
    (value % 360.0).clamp(0.0, 1.0)
}

pub fn normalized_to_rad(value: f32) -> f32 {
    value.clamp(0.0, 1.0) * std::f32::consts::TAU
}

pub fn rad_to_normalized(value: f32) -> f32 {
    (value % std::f32::consts::TAU).clamp(0.0, 1.0)
}

pub fn normalized_to_grad(value: f32) -> f32 {
    value.clamp(0.0, 1.0) * 400.0
}

pub fn grad_to_normalized(value: f32) -> f32 {
    (value % 400.0).clamp(0.0, 1.0)
}

pub fn deg_to_rad(deg: f32) -> f32 {
    deg.to_radians()
}

pub fn rad_to_deg(rad: f32) -> f32 {
    rad.to_degrees()
}

pub fn deg_to_grad(deg: f32) -> f32 {
    deg * 400.0 / 360.0
}

pub fn grad_to_deg(grad: f32) -> f32 {
    grad * 360.0 / 400.0
}

// Parse hex
pub fn parse_hex(hex: &str) -> Option<Color> {
    let hex = hex.trim_start_matches('#');

    let (rgb, alpha) = match hex.len() {
        6 => {
            let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
            let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
            let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
            ((r, g, b), 255)
        }
        8 => {
            let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
            let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
            let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
            let a = u8::from_str_radix(&hex[6..8], 16).ok()?;
            ((r, g, b), a)
        }
        _ => return None,
    };

    Some(Color::new(
        uint8_to_normalized(rgb.0),
        uint8_to_normalized(rgb.1),
        uint8_to_normalized(rgb.2),
        uint8_to_normalized(alpha),
    ))
}

pub fn color_to_hex(color: Color) -> String {
    let r = normalized_to_uint8(color.red);
    let g = normalized_to_uint8(color.green);
    let b = normalized_to_uint8(color.blue);

    if color.alpha < 0.99 {
        let a = normalized_to_uint8(color.alpha);
        format!("#{:02x}{:02x}{:02x}{:02x}", r, g, b, a)
    } else {
        format!("#{:02x}{:02x}{:02x}", r, g, b)
    }
}

pub fn format_decimal(value: f32, precision: usize) -> String {
    match precision {
        3 => format!("{:.3}", value),
        4 => format!("{:.4}", value),
        _ => format!("{:.2}", value),
    }
}

// Parse CSS
pub fn parse_css_color(input: &str) -> Option<Color> {
    let parsed = CssColor::from_html(input).ok()?;
    Some(Color::new(parsed.r, parsed.g, parsed.b, parsed.a))
}

pub fn color_to_css_rgb(color: &Color) -> String {
    CssColor::new(color.red, color.green, color.blue, color.alpha).to_css_rgb()
}

pub fn color_to_css_hsl(color: &Color) -> String {
    CssColor::new(color.red, color.green, color.blue, color.alpha).to_css_hsl()
}

pub fn color_to_css_hwb(color: &Color) -> String {
    CssColor::new(color.red, color.green, color.blue, color.alpha).to_css_hwb()
}

pub fn color_to_css_web_rgb_percentage(color: &Color) -> String {
    let red = format_decimal(normalized_to_percentage(color.red), 2);
    let green = format_decimal(normalized_to_percentage(color.green), 2);
    let blue = format_decimal(normalized_to_percentage(color.blue), 2);

    if color.alpha < 1.0 {
        let alpha = format_decimal(normalized_to_percentage(color.alpha), 2);
        format!("rgb({red}% {green}% {blue}% / {alpha}%)")
    } else {
        format!("rgb({red}% {green}% {blue}%)")
    }
}
