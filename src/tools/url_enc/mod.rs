/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod url_enc;
use gettextrs::pgettext;
pub use url_enc::UrlEncWidget;

define_tool!(
    widget: UrlEncWidget,
    id: "url_enc",
    title: pgettext("Tool Title", "URL Encoder & Decoder"),
    description: pgettext("Tool Description", "Encode and decode special characters in URLs"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "URL")),
    category: &ToolCategory::Encoders,
    keywords: [
        pgettext("Keyword", "unescape"),
        pgettext("Keyword", "web"),
        pgettext("Keyword", "link"),
        pgettext("Keyword", "address"),
        pgettext("Keyword", "uri"),
        pgettext("Keyword", "query")
    ],
);
