/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod diff;
mod text_diff;
use gettextrs::pgettext;
pub use text_diff::TextDiffWidget;

define_tool!(
    widget: TextDiffWidget,
    id: "text_diff",
    title: pgettext("Tool Title", "Text Diff"),
    description: pgettext("Tool Description", "Compare two text inputs and highlight the differences."),
    sidebar_title: None,
    category: &ToolCategory::Text,
    keywords: [
        pgettext("Keyword", "changes"),
        pgettext("Keyword", "modifications"),
    ],
);
