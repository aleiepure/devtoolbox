/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod color_blindness;
pub use color_blindness::ColorBlindnessWidget;
use gettextrs::pgettext;

define_tool!(
    widget: ColorBlindnessWidget,
    id: "color_blindness",
    title: pgettext("Tool Title", "Color Blindness Simulation"),
    description: pgettext("Tool Description", "Simulate color blindness effects on images"),
    sidebar_title: Some(pgettext("Tool Sidebar Title", "Color Blindness")),
    category: &ToolCategory::Graphics,
    keywords: [
        pgettext("Keyword", "simulation"),
        pgettext("Keyword", "daltonism"),
        pgettext("Keyword", "deficiency"),
        pgettext("Keyword", "vision"),
        pgettext("Keyword", "protanopia"),
        pgettext("Keyword", "deuteranopia"),
        pgettext("Keyword", "tritanopia"),
    ],
);
