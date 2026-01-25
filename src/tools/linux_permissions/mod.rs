/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod conversion;
mod linux_permissions;
use gettextrs::pgettext;
pub use linux_permissions::LinuxPermissionsWidget;

define_tool!(
    widget: LinuxPermissionsWidget,
    id: "linux_permissions",
    title: pgettext("Tool Title", "Linux Permissions"),
    description: pgettext("Tool Description", "Calculate permissions values"),
    sidebar_title: None,
    category: &ToolCategory::Converters,
    keywords: [
        pgettext("Keyword", "file"),
        "unix".to_string(),
        "linux".to_string(),
        pgettext("Keyword", "mode"),
        pgettext("Keyword", "access"),
        "chmod".to_string(),
    ],
);
