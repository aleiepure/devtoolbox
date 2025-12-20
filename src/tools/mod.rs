/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

pub mod macros;

pub trait Tool {
    fn metadata() -> ToolMetadata;
    fn create_view(&self) -> gtk::Widget;
}

#[derive(Clone, Copy)]
pub struct ToolMetadata {
    pub id: &'static str,
    pub title: &'static str,
    pub description: &'static str,
    pub category: &'static ToolCategory,
    pub icon: &'static str,
    pub keywords: &'static [&'static str],
}

use inventory;

use crate::tools::macros::ToolCategory;

inventory::collect!(ToolMetadata);

pub fn all_tools() -> impl Iterator<Item = &'static ToolMetadata> {
    inventory::iter::<ToolMetadata>()
}

pub mod config_format;
pub mod timestamp;
