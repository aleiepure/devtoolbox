/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod lipsum;
mod lorem;
use gettextrs::pgettext;
pub use lipsum::LipsumWidget;

define_tool!(
    widget: LipsumWidget,
    id: "lipsum",
    title: pgettext("Tool Title", "Lorem Ipsum"),
    description: pgettext("Tool Description", "Generate placeholder text"),
    sidebar_title: None,
    category: &ToolCategory::Generators,
    keywords: [
        pgettext("Keyword", "dummy"),
        pgettext("Keyword", "sample"),
        pgettext("Keyword", "filler"),
        pgettext("Keyword", "latin"),
    ],
);
