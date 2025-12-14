/*
 * macros.rs
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

use gettextrs::pgettext;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ToolCategory {
    Converters,
    Encoders,
    Formatters,
    Generators,
    Text,
    Graphics,
    Certificates,
}

impl ToolCategory {
    pub fn category_title(&self) -> String {
        match self {
            ToolCategory::Converters => pgettext("ToolCategory", "Converters").to_string(),
            ToolCategory::Encoders => pgettext("ToolCategory", "Encoders").to_string(),
            ToolCategory::Formatters => pgettext("ToolCategory", "Formatters").to_string(),
            ToolCategory::Generators => pgettext("ToolCategory", "Generators").to_string(),
            ToolCategory::Text => pgettext("ToolCategory", "Text").to_string(),
            ToolCategory::Graphics => pgettext("ToolCategory", "Graphics").to_string(),
            ToolCategory::Certificates => pgettext("ToolCategory", "Certificates").to_string(),
        }
    }

    pub const fn as_str(&self) -> &'static str {
        match self {
            ToolCategory::Converters => "converters",
            ToolCategory::Encoders => "encoders",
            ToolCategory::Formatters => "formatters",
            ToolCategory::Generators => "generators",
            ToolCategory::Text => "text",
            ToolCategory::Graphics => "graphics",
            ToolCategory::Certificates => "certificates",
        }
    }
}

#[macro_export]
macro_rules! define_tool {
    (
        $struct_name:ident,
        widget: $widget_name:path,
        id: $id:literal,
        title: $title:literal,
        description: $description:literal,
        category: $category:expr,
        icon: $icon:literal,
        keywords: [$($kw:literal),* $(,)?],
    ) => {
        pub struct $struct_name;

        pastey::paste! {
            pub static [<$struct_name:snake:upper _METADATA>]: $crate::tools::ToolMetadata =
                $crate::tools::ToolMetadata {
                    id: $id,
                    title: $title,
                    description: $description,
                    category: $category,
                    icon: $icon,
                    keywords: &[$($kw),*],
                };
        }

        impl $crate::tools::Tool for $struct_name {
            fn metadata() -> $crate::tools::ToolMetadata {
                pastey::paste! {
                    [<$struct_name:snake:upper _METADATA>]
                }
            }

            fn create_view(&self) -> gtk::Widget {
                use gtk::prelude::*;
                <$widget_name>::new(&Self::metadata()).upcast()
            }
        }
    };
}
