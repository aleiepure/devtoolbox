#! /bin/bash

# new-tool.sh
#
# Script to create a new tool directory with boilerplate files. See CONTRIBUTING.md
# for details.
#
# Copyright (C) 2025 Alessandro Iepure
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

# Check if tool ID is provided
if [ -z "$1" ]; then
    echo "Usage: ./create-tool.sh <tool-id>"
    echo "Example: ./create-tool.sh my_new_tool"
    exit 1
fi

TOOL_ID="$1"
TOOL_ID_UPPER=$(echo "$TOOL_ID" | tr '[:lower:]' '[:upper:]')
TOOL_ID_PASCAL=$(echo "$TOOL_ID" | sed -r 's/(^|_)([a-z])/\U\2/g')
TOOL_ID_WIDGET="${TOOL_ID_PASCAL}Widget"

TOOL_DIR="src/tools/$TOOL_ID"

# Check if tool already exists
if [ -d "$TOOL_DIR" ]; then
    echo "Error: Tool '$TOOL_ID' already exists at $TOOL_DIR"
    exit 1
fi

echo "Creating tool: $TOOL_ID"
echo ""

# MARK: Create tool directory
mkdir -p "$TOOL_DIR"

# MARK: Create mod.rs
cat > "$TOOL_DIR/mod.rs" << EOF
/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod $TOOL_ID;
pub use $TOOL_ID::$TOOL_ID_WIDGET;
use gettextrs::pgettext;

define_tool!(
    widget: $TOOL_ID_WIDGET,
    id: "$TOOL_ID",
    title: pgettext("Tool Title", ""),  // TODO: add title
    description: pgettext("Tool Description", ""), // TODO: add description
    sidebar_title: None, // Some(pgettext("Tool Sidebar Title", "")),
    category: &ToolCategory::Converters, // TODO: Change as needed
    keywords: ["".to_string()], // TODO: add keywords
);
EOF
echo "$TOOL_DIR/mod.rs: file created."

# MARK: Create rust file
cat > "$TOOL_DIR/$TOOL_ID.rs" << EOF
/*
 * $TOOL_ID.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/$TOOL_ID/$TOOL_ID.ui")]
    #[properties(wrapper_type = super::$TOOL_ID_WIDGET)]
    pub struct $TOOL_ID_WIDGET {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        // Properties (if not needed, remove Properties derive and this section)
        // #[property(get, set, type = bool, default = false)]
        // example_property: RefCell<bool>,

        // Other fields
        // example_variable: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for $TOOL_ID_WIDGET {
        const NAME: &'static str = "$TOOL_ID_WIDGET";
        type Type = super::$TOOL_ID_WIDGET;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl $TOOL_ID_WIDGET {
        // Template callbacks and closures
        // #[template_callback]
        // fn on_signal_signalname_widgetid(&self) {}

        // Other methods
    }

    #[glib::derived_properties] // Remove this line if no properties
    impl ObjectImpl for $TOOL_ID_WIDGET {
        fn constructed(&self) {
            self.parent_constructed();
            // Initialization code here, delete whole function if not needed
        }

        // Delete this whole block if not defining custom signals
        fn signals() -> &'static [glib::subclass::Signal] {
            static SIGNALS: &[glib::subclass::Signal] = &[
                // Define signals here
                // glib::subclass::Signal::builder("signal-name")
                //     .param_types(&[])
                //     .build(),
            ];
            SIGNALS
        }
    }
    
    impl WidgetImpl for $TOOL_ID_WIDGET {}
    impl BinImpl for $TOOL_ID_WIDGET {}
}

glib::wrapper! {
    pub struct $TOOL_ID_WIDGET(ObjectSubclass<imp::$TOOL_ID_WIDGET>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl $TOOL_ID_WIDGET {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
EOF
echo "$TOOL_DIR/$TOOL_ID.rs: file created."

# MARK: Create blueprint file
cat > "$TOOL_DIR/$TOOL_ID.blp" << EOF
/*
 * $TOOL_ID.blp
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/
using Gtk 4.0;
using Adw 1;

template \$$TOOL_ID_WIDGET : Adw.Bin {
  Adw.ToastOverlay toast_overlay {
    child: ScrolledWindow {
      child: Adw.Clamp {
        vexpand: true;
        maximum-size: 1200;
        tightening-threshold: 600;

        child: Box {
          orientation: vertical;
          spacing: 24;
          margin-bottom: 12;
          margin-top: 12;

          // MARK: - Tool Settings
          Adw.PreferencesGroup {
            title: _("Options");
            // Define Rows based on tool functionality, remove preferences group
            // if not needed.
          }

          // MARK: - Tool Main Content
          Box {
            Label {
              label: "Replace this box/label with the tool main content.";
            }
          }
        };
      };
    };
  }
}
EOF
echo "$TOOL_DIR/$TOOL_ID.blp: file created."

# MARK: Update src/tools/mod.rs
TOOLS_MOD="src/tools/mod.rs"

# Add module declaration
if ! grep -q "^pub mod $TOOL_ID;" "$TOOLS_MOD"; then
    LAST_MOD_LINE=$(grep -n "^pub mod " "$TOOLS_MOD" | tail -1 | cut -d: -f1)
    sed -i "${LAST_MOD_LINE}a pub mod $TOOL_ID;" "$TOOLS_MOD"
fi

# Add to ALL_TOOLS array
if ! grep -q "${TOOL_ID}::${TOOL_ID_UPPER}_TOOL_METADATA" "$TOOLS_MOD"; then
    # Add before the comment line "// TODO: add new tools here"
    sed -i "/\/\/ TODO: add new tools here/i\        \&${TOOL_ID}::${TOOL_ID_UPPER}_TOOL_METADATA," "$TOOLS_MOD"
fi
echo "$TOOLS_MOD: file updated."

# MARK: Update gresource.xml
GRESOURCE="src/devtoolbox.gresource.xml"

# Add icon entry
if ! grep -q "alias=\"${TOOL_ID}_symbolic.svg\"" "$GRESOURCE"; then
    # Find the last tool icon line (before </gresource> in icons section)
    sed -i "/<!-- Tool icons -->/,/<\/gresource>/ {
        /<\/gresource>/i\    <file compressed=\"true\" alias=\"${TOOL_ID}-symbolic.svg\">..\/data\/icons\/symbolic\/tools\/${TOOL_ID}-symbolic.svg<\/file>
    }" "$GRESOURCE"
fi

# Add UI entry
if ! grep -q "tools/${TOOL_ID}/${TOOL_ID}.ui" "$GRESOURCE"; then
    # Find the Tools comment section and add before next closing tag
    sed -i "/<!-- Tools -->/,/^  <\/gresource>/ {
        /^  <\/gresource>/i\    <file>tools\/${TOOL_ID}\/${TOOL_ID}.ui<\/file>
    }" "$GRESOURCE"
fi
echo "$GRESOURCE: file updated."

# MARK: Update src/meson.build
MESON_BUILD="src/meson.build"

if ! grep -q "'tools/${TOOL_ID}/${TOOL_ID}.blp'" "$MESON_BUILD"; then
    # Find the last line in blueprint_files that ends with .blp', and add after it
    LAST_BLUEPRINT_LINE=$(grep -n "\.blp'," "$MESON_BUILD" | tail -1 | cut -d: -f1)
    sed -i "${LAST_BLUEPRINT_LINE}a\  'tools/${TOOL_ID}/${TOOL_ID}.blp'," "$MESON_BUILD"
fi
echo "$MESON_BUILD: file updated."

# MARK: Update gschema.xml
GSETTINGS="data/me.iepure.Devtoolbox.gschema.xml"

if ! grep -q "<choice value='${TOOL_ID}'/>" "$GSETTINGS"; then
    # Add before the </choices> tag for last-tool key
    sed -i "/<key name=\"last-tool\"/,/<\/choices>/ {
        /<\/choices>/i\                <choice value=\"${TOOL_ID}\"/>
    }" "$GSETTINGS"
fi
echo "$GSETTINGS: file updated."

# MARK: Update src/core/window.rs
WINDOW_RS="src/core/window.rs"

if ! grep -q "\"${TOOL_ID}\"" "$WINDOW_RS"; then
    # Find the last tool case in the match statement and add before the _ => panic line
    sed -i "/fn create_tool_view/,/_ => {$/ {
        /_ => {$/i\                \"${TOOL_ID}\" => {\n                    use crate::tools::${TOOL_ID}::${TOOL_ID_WIDGET};\n                    ${TOOL_ID_WIDGET}::new().upcast()\n                }
    }" "$WINDOW_RS"
fi
echo "$WINDOW_RS: file updated."

echo ""
echo "Boilerplate creation for tool '$TOOL_ID' completed."
echo "Manual steps:"
echo "1. Add icon: data/resources/icons/symbolic/tools/${TOOL_ID}_symbolic.svg"
echo "2. Fill in metadata in src/tools/${TOOL_ID}/mod.rs"
echo "3. Implement tool UI in src/tools/${TOOL_ID}/${TOOL_ID}.blp"
echo "4. Implement tool logic in src/tools/${TOOL_ID}/${TOOL_ID}.rs"
