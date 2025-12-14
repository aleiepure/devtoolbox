/*
 * mod.rs
 *
 * Copyright (C) 2022-2025 Alessandro Iepure
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod config_format;
pub use config_format::ConfigFormatWidget;

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
