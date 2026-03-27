/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod color_conversion;
mod color_spaces;
pub use color_spaces::ColorSpacesWidget;
use gettextrs::pgettext;

define_tool!(
    widget: ColorSpacesWidget,
    id: "color_spaces",
    title: pgettext("Tool Title", "Color Spaces"),
    description: pgettext("Tool Description", "Convert colors between different color spaces"),
    sidebar_title: None,
    category: &ToolCategory::Graphics,
    keywords: [
        "rgba".to_string(),
        "hex".to_string(),
        "hsl".to_string(),
        "cmyk".to_string(),
        "hsv".to_string(),
        "hwb".to_string(),
        pgettext("Keyword", "format"),
        pgettext("Keyword", "conversion"),
        pgettext("Keyword", "palette"),
    ],
);
