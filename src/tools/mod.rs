/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

pub mod config_format;
pub mod macros;
pub mod timestamp;

use once_cell::sync::Lazy;

use crate::tools::macros::ToolCategory;

#[derive(Clone)]
pub struct ToolMetadata {
    pub id: &'static str,
    pub title: String,
    pub description: String,
    pub sidebar_title: Option<String>,
    pub category: &'static ToolCategory,
    pub keywords: &'static [String],
}

pub static ALL_TOOLS: Lazy<Vec<&'static ToolMetadata>> = Lazy::new(|| {
    vec![
        &config_format::CONFIG_FORMAT_TOOL_METADATA,
        &timestamp::TIMESTAMP_TOOL_METADATA,
    ] // TODO: add new tools here
});

pub fn all_tools() -> impl Iterator<Item = &'static ToolMetadata> {
    ALL_TOOLS.iter().copied()
}
