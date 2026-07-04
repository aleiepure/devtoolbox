/*
 * macros.rs
 *
 * Copyright (C) 2025-2026 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use gettextrs::pgettext;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
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
            ToolCategory::Encoders => pgettext("ToolCategory", "Encoders & Decoders").to_string(),
            ToolCategory::Formatters => pgettext("ToolCategory", "Formatters").to_string(),
            ToolCategory::Generators => pgettext("ToolCategory", "Generators").to_string(),
            ToolCategory::Text => pgettext("ToolCategory", "Text").to_string(),
            ToolCategory::Graphics => pgettext("ToolCategory", "Graphics").to_string(),
            ToolCategory::Certificates => pgettext("ToolCategory", "Certificates").to_string(),
        }
    }
}

#[macro_export]
macro_rules! define_tool {
    (
        widget: $widget_name:path,
        id: $id:literal,
        title: $title:expr,
        description: $description:expr,
        sidebar_title: $sidebar_title:expr,
        category: $category:expr,
        keywords: [$($kw:expr),* $(,)?],
    ) => {
        pastey::paste! {
            pub static [<$id:snake:upper _TOOL_METADATA>]: once_cell::sync::Lazy<$crate::tools::ToolMetadata> =
                once_cell::sync::Lazy::new(|| $crate::tools::ToolMetadata {
                    id: $id,
                    title: $title,
                    description: $description,
                    sidebar_title: $sidebar_title,
                    category: $category,
                    icon_name: concat!($id, "-symbolic"),
                    keywords: Box::leak(Box::new([$($kw),*])),
                });
        }
    };
}

#[macro_export]
macro_rules! connect_imp_signal {
    ($self:ident, $handler_field:ident, $widget_field:ident, $signal:literal, $callback:ident) => {{
        use gtk::prelude::ObjectExt as _;

        let obj_weak = $self.obj().downgrade();
        let handler_id = $self.$widget_field.connect_local($signal, true, move |_| {
            if let Some(obj) = obj_weak.upgrade() {
                obj.imp().$callback();
            }
            None
        });
        $self.$handler_field.replace(Some(handler_id));
    }};
}

#[macro_export]
macro_rules! connect_imp_signals {
    ($self:ident; $( $handler_field:ident <= $widget_field:ident, $signal:literal => $callback:ident );+ $(;)?) => {
        $(
            connect_imp_signal!($self, $handler_field, $widget_field, $signal, $callback);
        )+
    };
}
