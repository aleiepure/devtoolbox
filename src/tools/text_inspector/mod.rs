/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod string_cases;
mod text_inspector;
use gettextrs::pgettext;
pub use text_inspector::TextInspectorWidget;

define_tool!(
    widget: TextInspectorWidget,
    id: "text_inspector",
    title: pgettext("Tool Title", "Text Inspector & Case Converter"),
    description: pgettext("Tool Description", "View statistics and convert case of text"),
    sidebar_title: None,
    category: &ToolCategory::Text,
    keywords: [
        pgettext("Keyword", "analyze"),
        pgettext("Keyword", "uppercase"),
        pgettext("Keyword", "lowercase"),
        pgettext("Keyword", "capitalize"),
        pgettext("Keyword", "count"),
        pgettext("Keyword", "words"),
        pgettext("Keyword", "characters"),
        pgettext("Keyword", "lines"),
    ],
);
