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

A tool is a collection of information about a functionality available in the app. It's made up of several metadata and a widget that implements the UI.

Each tool has its own module inside `src/tools/<tool-id>`. Inside each tool has the following files:

- `mod.rs`
- `<tool-id>.rs`
- `<tool-id>.blp`
- any other file needed to implement its logic

Inside `mod.rs` define the tool's metadata via the `define_tool!` macro. It takes the following parameters:

- `widget`: Object type of the widget to be shown
- `id`: unique name for the tool inside the app (snake_case)
- `title`: title shown at the top of the widget. If `sidebar_title` is not provided, also used for the sidebar
- `description`: subtitle shown under the title at the top of the widget. Also used for sidebar tooltip on hover
- `sidebar_title`: override the title shown in the sidebar. Set to `None` if not required
- `category`: one of the available categories. Affects the position in the sidebar and search
- `keywords`: keywords for searching

Tool icon in the sidebar is an svg named `<tool_id>_symbolic.svg` placed in `data/icons/symbolic/tools/`. Make sure to add an entry in the `gresource.xml` file as well.

Make sure to add a line in `src/meson.build` around line 51 to compile the tool's blueprint file and update the `gresource.xml`
with a new line for the tool.

In `gschema.xml` add a choice for the `last-tool` key (around line 25) with the tool id.

In `src/tools/mod.rs` add a new line in the `ALL_TOOLS` array formatted as such: `&<tool_id>::<TOOL_ID>_TOOL_METADATA,`.

All tools need to have a toast overlay, the tool title widget at the top (bound to title and description from metadata), 
options if needed and the rest of the ui. Make sure width is consistent across all tools.

> [!TIP]
> To simplify these steps, use the `new-tool.sh` script included in the repo.
> 
> `./new-tool.sh <tool_id>`

<!-- ## Translations

Translatable strings are gathered via gettext. List all files that contain translatable 
strings in `po/POTFILES.in`. List all supported languages in `po/LINGUAS`.

Generate the translation template with `` in a Flatpak build terminal. Update the
current translations with the new template by calling `` in a Flatpak build terminal.

After committing, WebLate will pick up the changes. Use the website for actual
translation work. -->
