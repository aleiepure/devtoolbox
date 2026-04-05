/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod generator;
mod qrcode;
use gettextrs::pgettext;
pub use qrcode::QrcodeWidget;

define_tool!(
    widget: QrcodeWidget,
    id: "qrcode",
    title: pgettext("Tool Title", "QR Code"),
    description: pgettext("Tool Description", "Generate QR codes with various content"),
    sidebar_title: None,
    category: &ToolCategory::Generators,
    keywords: [
        pgettext("Keyword", "barcode"),
        pgettext("Keyword", "matrix"),
        pgettext("Keyword", "image"),
    ],
);
