/*
 * wrap_mode.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

pub enum WrapMode {
    None,
    Char,
    Word,
    WordChar,
}

impl From<WrapMode> for gtk::WrapMode {
    fn from(mode: WrapMode) -> Self {
        match mode {
            WrapMode::None => gtk::WrapMode::None,
            WrapMode::Char => gtk::WrapMode::Char,
            WrapMode::Word => gtk::WrapMode::Word,
            WrapMode::WordChar => gtk::WrapMode::WordChar,
        }
    }
}

impl From<gtk::WrapMode> for WrapMode {
    fn from(mode: gtk::WrapMode) -> Self {
        match mode {
            gtk::WrapMode::None => WrapMode::None,
            gtk::WrapMode::Char => WrapMode::Char,
            gtk::WrapMode::Word => WrapMode::Word,
            gtk::WrapMode::WordChar => WrapMode::WordChar,
            _ => WrapMode::None,
        }
    }
}

impl From<String> for WrapMode {
    fn from(value: String) -> Self {
        match value.as_str() {
            "none" => WrapMode::None,
            "char" => WrapMode::Char,
            "word" => WrapMode::Word,
            "word-char" => WrapMode::WordChar,
            _ => WrapMode::None,
        }
    }
}

impl From<&str> for WrapMode {
    fn from(value: &str) -> Self {
        match value {
            "none" => WrapMode::None,
            "char" => WrapMode::Char,
            "word" => WrapMode::Word,
            "word-char" => WrapMode::WordChar,
            _ => WrapMode::None,
        }
    }
}
