/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod uuid;
use gettextrs::pgettext;
pub use uuid::UuidWidget;

define_tool!(
    widget: UuidWidget,
    id: "uuid",
    title: pgettext("Tool Title", "UUID Generator"),
    description: pgettext("Tool Description", "Generate Universal Unique IDs"),
    sidebar_title: Some("UUID".to_string()),
    category: &ToolCategory::Generators,
    keywords: [
        pgettext("Keyword", "identifier"),
        pgettext("Keyword", "random"),
    ],
);
