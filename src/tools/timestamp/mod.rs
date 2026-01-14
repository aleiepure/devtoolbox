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
    title: pgettext("Tool Title", "Timestamp"),
    description: pgettext("Tool Description", "A tool to work with timestamps."),
    sidebar_title: None,
    category: &ToolCategory::Formatters,
    keywords: ["timestamp", "time", "conversion"],
);
