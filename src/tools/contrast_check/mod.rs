/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod contrast_check;
pub use contrast_check::ContrastCheckWidget;
use gettextrs::pgettext;

define_tool!(
    widget: ContrastCheckWidget,
    id: "contrast_check",
    title: pgettext("Tool Title", "Contrast Checker"),
    description: pgettext("Tool Description", "Check color combinations for WCAG compliance"),
    sidebar_title: None,
    category: &ToolCategory::Graphics,
    keywords: [
        pgettext("Keyword", "accessibility"),
        pgettext("Keyword", "ratio"),
    ],
);
