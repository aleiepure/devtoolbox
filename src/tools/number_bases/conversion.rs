/*
 * conversion.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

#[derive(Debug, Clone, Copy)]
pub enum Base {
    Decimal,
    Binary,
    Octal,
    Hexadecimal,
    Ascii,
    Utf8,
}

pub struct ConversionResult {
    pub decimal: String,
    pub binary: String,
    pub octal: String,
    pub hexadecimal: String,
    pub ascii: String,
    pub utf8: String,
}

impl ConversionResult {
    fn empty() -> Self {
        Self {
            decimal: String::new(),
            binary: String::new(),
            octal: String::new(),
            hexadecimal: String::new(),
            ascii: String::new(),
            utf8: String::new(),
        }
    }
}

pub fn do_conversion(input: &str, from: Base) -> ConversionResult {
    let value = match from {
        Base::Ascii | Base::Utf8 => input.chars().next().map(|c| c as u32),
        Base::Decimal => u32::from_str_radix(input.trim(), 10).ok(),
        Base::Binary => u32::from_str_radix(input.trim(), 2).ok(),
        Base::Octal => u32::from_str_radix(input.trim(), 8).ok(),
        Base::Hexadecimal => u32::from_str_radix(input.trim(), 16).ok(),
    };

    let Some(value) = value else {
        return ConversionResult::empty();
    };

    ConversionResult {
        decimal: value.to_string(),
        binary: format!("{:b}", value),
        octal: format!("{:o}", value),
        hexadecimal: format!("{:X}", value),
        ascii: if value <= 127 && value != 0 {
            char::from_u32(value).unwrap_or(' ').to_string()
        } else {
            String::new()
        },
        utf8: if value != 0 {
            char::from_u32(value)
                .map(|c| c.to_string())
                .unwrap_or_default()
        } else {
            String::new()
        },
    }
}
