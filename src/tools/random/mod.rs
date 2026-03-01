/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod random;
use gettextrs::pgettext;
pub use random::RandomWidget;

define_tool!(
    widget: RandomWidget,
    id: "random",
    title: pgettext("Tool Title", "Random Generator"),
    description: pgettext("Tool Description", "Generate random numbers, strings, and passphrases"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "Random")),
    category: &ToolCategory::Generators,
    keywords: [
        pgettext("Keyword", "password"),
        pgettext("Keyword", "token"),
        pgettext("Keyword", "entropy"),
        pgettext("Keyword", "secure"),
    ],
);
