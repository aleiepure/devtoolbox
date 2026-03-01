/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

pub mod base64;
pub mod config_format;
pub mod cron_gen;
pub mod cron_parser;
pub mod html_enc;
pub mod linux_permissions;
pub mod lipsum;
pub mod macros;
pub mod number_bases;
pub mod random;
pub mod timestamp;
pub mod url_enc;
pub mod uuid;

use once_cell::sync::Lazy;

use crate::tools::macros::ToolCategory;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct ToolMetadata {
    pub id: &'static str,
    pub title: String,
    pub description: String,
    pub sidebar_title: Option<String>,
    pub category: &'static ToolCategory,
    pub keywords: &'static [String],
}

pub static ALL_TOOLS: Lazy<Vec<&'static ToolMetadata>> = Lazy::new(|| {
    let mut tools = vec![
        &*config_format::CONFIG_FORMAT_TOOL_METADATA,
        &*timestamp::TIMESTAMP_TOOL_METADATA,
        &*number_bases::NUMBER_BASES_TOOL_METADATA,
        &*cron_parser::CRON_PARSER_TOOL_METADATA,
        &*cron_gen::CRON_GEN_TOOL_METADATA,
        &*linux_permissions::LINUX_PERMISSIONS_TOOL_METADATA,
        &*html_enc::HTML_ENC_TOOL_METADATA,
        &*base64::BASE64_TOOL_METADATA,
        &*url_enc::URL_ENC_TOOL_METADATA,
        &*lipsum::LIPSUM_TOOL_METADATA,
        &*uuid::UUID_TOOL_METADATA,
        &*random::RANDOM_TOOL_METADATA,
    ]; // TODO: add new tools here
    tools.sort_by(|a, b| a.category.cmp(&b.category));
    tools
});

pub fn all_tools() -> impl Iterator<Item = &'static ToolMetadata> {
    ALL_TOOLS.iter().copied()
}
