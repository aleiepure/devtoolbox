/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod config_format;
pub use config_format::ConfigFormatWidget;
use gettextrs::pgettext;

mod convertion;

define_tool!(
    widget: ConfigFormatWidget,
    id: "config_format",
    title: pgettext("Tool Title", "Configuration Format Converter"),
    description: pgettext("Tool Description", "Convert configuration files between different formats"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "Configuration Format")),
    category: &ToolCategory::Converters,
    keywords: [
        pgettext("Keyword", "config"),
        pgettext("Keyword", "format"),
        pgettext("Keyword", "development"),
        "json".to_string(),
        "yaml".to_string(),
        "toml".to_string()],
);
