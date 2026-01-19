/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod conversion;
mod number_bases;

pub use gettextrs::pgettext;
pub use number_bases::NumberBasesWidget;

define_tool!(
    widget: NumberBasesWidget,
    id: "number_bases",
    title: pgettext("Tool Title", "Number Bases"),
    description: pgettext("Tool Description", "Convert numbers across different bases."),
    sidebar_title: None,
    category: &ToolCategory::Converters,
    keywords: [
        "ascii".to_string(),
        "utf-8".to_string(),
        "utf8".to_string(),
        pgettext("Keyword", "representation"),
        pgettext("Keyword", "binary"),
        pgettext("Keyword", "decimal"),
        pgettext("Keyword", "hexadecimal"),
        pgettext("Keyword", "octal"),
        pgettext("Keyword", "integer")
    ],
);
