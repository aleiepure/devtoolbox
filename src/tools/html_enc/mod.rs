/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod html_enc;
use gettextrs::pgettext;
pub use html_enc::HtmlEncWidget;

define_tool!(
    widget: HtmlEncWidget,
    id: "html_enc",
    title: pgettext("Tool Title", "HTML Encoder & Decoder"),
    description: pgettext("Tool Description", "Encode and decode special characters in HTML"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "HTML")),
    category: &ToolCategory::Encoders,
    keywords: [
        pgettext("Keyword", "escape"),
        pgettext("Keyword", "markup"),
        pgettext("Keyword", "text"),
        pgettext("Keyword", "website")
    ],
);
