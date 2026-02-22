/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod cron;
mod cron_gen;
pub use cron_gen::CronGenWidget;
use gettextrs::pgettext;

define_tool!(
    widget: CronGenWidget,
    id: "cron_gen",
    title: pgettext("Tool Title", "CRON Expressions"),
    description: pgettext("Tool Description", "Generate CRON expressions"),
    sidebar_title: None,
    category: &ToolCategory::Generators,
    keywords: [
        pgettext("Keyword", "schedule"),
        pgettext("Keyword", "parser"),
        pgettext("Keyword", "convert"),
        pgettext("Keyword", "time"),
        pgettext("Keyword", "date"),
        pgettext("Keyword", "job"),
        "linux".to_string(),
        "unix".to_string(),
    ],
);
