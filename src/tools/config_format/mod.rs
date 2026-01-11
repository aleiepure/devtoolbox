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

mod convertion;
pub use convertion::ConfigFormat;
pub use convertion::{
    json_to_toml, json_to_yaml, toml_to_json, toml_to_yaml, yaml_to_json, yaml_to_toml,
};
pub use convertion::{validate_json, validate_toml, validate_yaml};

define_tool!(
    ConfigFormatTool,
    widget: ConfigFormatWidget,
    id: "config_format",
    title: "Configuration Format",
    description: "A tool to format configuration files.",
    category: &ToolCategory::Converters,
    icon: "document-edit",
    keywords: ["config", "format", "development"],
);

inventory::submit! {
    CONFIG_FORMAT_TOOL_METADATA
}
