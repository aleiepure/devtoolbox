# Contributing

This app is written in Rust.

## Dependencies

|Dependency|Description|
|---|---|
|`gtk-rs`|GTK bindings for Rust|


## Packaging

The only supported packaging method is Flatpak. 

## Add a custom widget

Each custom widget has its owm module inside `src/core/widgets/<widget-name>`.

Add a `subdir('<widget-name>')` statement in `src/core/widgets/meson.build`.

Each widget contains: 

- `mod.rs`
- `<widget-name>.blp`
- `<widget-name>.rs`

~~## Adding a new tool (TBD)~~

~~Each tool has its own module inside `src/tools/<tool-id>`. Inside each tool has the following files:~~

- `mod.rs`
- `ui.rs`
- `logic.rs`
- `<tool-id>.blp`

~~Add a `subdir('<tool-id>')` statement in `src/tools/meson.build`.~~
~~Add a choice in the gschema for key `last-tool` with tool id.~~

## Translations

Translatable strings are gathered via gettext. List all files that contain translatable 
strings in `po/POTFILES.in`. List all supported languages in `po/LINGUAS`.

Generate the translation template with `` in a Flatpak build terminal. Update the
current translations with the new template by calling `` in a Flatpak build terminal.

After committing, WebLate will pick up the changes. Use the website for actual
translation work.
