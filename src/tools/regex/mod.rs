/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod regex;
use gettextrs::pgettext;
pub use regex::RegexWidget;

define_tool!(
    widget: RegexWidget,
    id: "regex",
    title: pgettext("Tool Title", "Regular Expression Tester"),
    description: pgettext("Tool Description", "Test your regular expressions in text"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "Regex Tester")),
    category: &ToolCategory::Text,
    keywords: [
        pgettext("Keyword", "find"),
        pgettext("Keyword", "search"),
        pgettext("Keyword", "match"),
        pgettext("Keyword", "pattern"),
    ],
);
