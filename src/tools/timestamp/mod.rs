/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod timestamp;
use gettextrs::pgettext;
pub use timestamp::TimestampWidget;

define_tool!(
    widget: TimestampWidget,
    id: "timestamp",
    title: pgettext("Tool Title", "Timestamp Converter"),
    description: pgettext("Tool Description", "Convert timestamps between different formats"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "Timestamp")),
    category: &ToolCategory::Converters,
    keywords: [
        pgettext("Keyword", "epoch"),
        pgettext("Keyword", "time"),
        pgettext("Keyword", "format"),
        pgettext("Keyword", "parse"),
        pgettext("Keyword", "datetime"),
        pgettext("Keyword", "calendar"),
        "unix".to_string(),
        pgettext("Keyword", "date"),
        pgettext("Keyword", "format"),
        pgettext("Keyword", "short"),
        pgettext("Keyword", "long"),
        "ISO".to_string(),
        "RFC".to_string(),
        pgettext("Keyword", "years"),
        pgettext("Keyword", "months"),
        pgettext("Keyword", "days"),
        pgettext("Keyword", "hours"),
        pgettext("Keyword", "minutes"),
        pgettext("Keyword", "seconds"),
        pgettext("Keyword", "timezone"),
        pgettext("Keyword", "now"),
    ],
);
