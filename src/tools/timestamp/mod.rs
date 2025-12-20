/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod timestamp;
pub use timestamp::TimestampWidget;

define_tool!(
    TimestampTool,
    widget: TimestampWidget,
    id: "timestamp",
    title: "Timestamp",
    description: "A tool to work with timestamps.",
    category: &ToolCategory::Formatters,
    icon: "document-edit",
    keywords: ["timestamp", "time", "conversion"],
);

inventory::submit! {
    TIMESTAMP_TOOL_METADATA
}
