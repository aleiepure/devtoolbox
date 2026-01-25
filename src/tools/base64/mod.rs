/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod base64;
pub use base64::Base64Widget;
use gettextrs::pgettext;

define_tool!(
    widget: Base64Widget,
    id: "base64",
    title: pgettext("Tool Title", "Base64 Encoder & Decoder"),
    description: pgettext("Tool Description", "Encode and decode text in Base64 format"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "Base64")),
    category: &ToolCategory::Encoders,
    keywords: [
        pgettext("Keyword", "string"),
        pgettext("Keyword", "text"),
        pgettext("Keyword", "data")
    ],
);
