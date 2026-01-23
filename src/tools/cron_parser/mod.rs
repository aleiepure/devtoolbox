/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod cron_parser;
pub use cron_parser::CronParserWidget;

mod specifier_row;
pub use specifier_row::SpecifierRow;

use gettextrs::pgettext;

define_tool!(
    widget: CronParserWidget,
    id: "cron_parser",
    title: pgettext("Tool Title", "CRON Parser"),
    description: pgettext("Tool Description", "Convert CRON expressions to human-readable format"),
    sidebar_title: None,
    category: &ToolCategory::Converters,
    keywords: [
        "cron".to_string(),
        pgettext("Keyword", "schedule"),
        pgettext("Keyword", "parser"),
        pgettext("Keyword", "time"),
        pgettext("Keyword", "date"),
        pgettext("Keyword", "job"),
        "linux".to_string(),
        "unix".to_string(),
    ],
);
