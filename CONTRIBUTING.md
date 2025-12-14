# Contributing

This app is written in Rust.

## Dependencies

|Dependency|Description|
|---|---|
|`gettextrs`|Provides gettext functionality for translations|
|`gtk-rs`|GTK bindings for Rust|
|`inventory`|Used to auto-register tools without explicitly listing them|


## Packaging

The only supported packaging method is Flatpak. 

## Add a custom widget

Each custom widget has its owm module inside `src/core/widgets/<widget-name>`.

Add a `subdir('<widget-name>')` statement in `src/core/widgets/meson.build`.

Each widget contains: 

- `mod.rs`
- `<widget-name>.blp`
- `<widget-name>.rs`

Add an entry in gresource for the `.ui` file and in `src/meson.build` to compile the blueprint.

## Adding a new tool

A tool is a collection of information about a functionality available in the app. It's made up of several metadata
and a widget that implements the UI.

Each tool has its own module inside `src/tools/<tool-id>`. Inside each tool has the following files:

- `mod.rs`
- `<tool-id>.rs`
- `<tool-id>.blp`

Refer to the other tools for the contents of each file.
Add a choice in the gschema for key `last-tool` with tool id.
Add an entry in `src/core/window.rs` in function `create_tool_view(...)` for the new tool's id.
Add an entry in gresource for the `.ui` file and in `src/meson.build` to compile the blueprint.

<!-- ## Translations

Translatable strings are gathered via gettext. List all files that contain translatable 
strings in `po/POTFILES.in`. List all supported languages in `po/LINGUAS`.

Generate the translation template with `` in a Flatpak build terminal. Update the
current translations with the new template by calling `` in a Flatpak build terminal.

After committing, WebLate will pick up the changes. Use the website for actual
translation work. -->
