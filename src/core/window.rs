/* window.rs
 *
 * Copyright (C) 2025-2026 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gio, glib, CompositeTemplate};

mod imp {
    use adw::prelude::AdwDialogExt;
    use gettextrs::gettext;
    use gtk::gio::Settings;
    use std::cell::RefCell;
    use std::collections::HashMap;

    use crate::config::APP_ID;
    use crate::tools::{all_tools, ToolMetadata};

    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/me/iepure/devtoolbox/core/ui/window.ui")]
    pub struct DevtoolboxWindow {
        // Template widgets
        #[template_child]
        overlay_split_view: TemplateChild<adw::OverlaySplitView>,

        #[template_child]
        content_header_bar: TemplateChild<adw::HeaderBar>,

        #[template_child]
        toggle_sidebar_button: TemplateChild<gtk::ToggleButton>,

        #[template_child]
        menu_button: TemplateChild<gtk::MenuButton>,

        #[template_child]
        favorite_popover: TemplateChild<gtk::Popover>,

        #[template_child]
        favorite_view_stack: TemplateChild<adw::ViewStack>,

        #[template_child]
        favorite_listbox: TemplateChild<gtk::ListBox>,

        #[template_child]
        sidebar_listbox: TemplateChild<gtk::ListBox>,

        #[template_child]
        mark_favorite_button: TemplateChild<gtk::Button>,

        #[template_child]
        content_view_stack: TemplateChild<adw::ViewStack>,

        #[template_child]
        show_search_button: TemplateChild<gtk::ToggleButton>,

        #[template_child]
        search_bar: TemplateChild<gtk::SearchBar>,

        #[template_child]
        search_entry: TemplateChild<gtk::SearchEntry>,

        #[template_child]
        sidebar_view_stack: TemplateChild<adw::ViewStack>,

        // Other fields
        loaded_tools: RefCell<HashMap<String, gtk::Widget>>,
        updating_search_mode: RefCell<bool>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for DevtoolboxWindow {
        const NAME: &'static str = "DevtoolboxWindow";
        type Type = super::DevtoolboxWindow;
        type ParentType = adw::ApplicationWindow;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl DevtoolboxWindow {
        /// Callback for when the window is mapped (shown) on the screen.
        #[template_callback]
        fn on_signal_map(&self) {
            self.sidebar_listbox.grab_focus();
            self.content_view_stack
                .visible_child()
                .unwrap()
                .grab_focus();
        }

        /// Callback for when a tool is activated from the favorites menu.
        #[template_callback]
        fn on_signal_row_activated_favorite_listbox(&self, row: &gtk::ListBoxRow) {
            let tool_id = row.widget_name().to_string();
            self.load_and_show_tool(&tool_id);
            self.favorite_popover.popdown();
        }

        /// Callback for when the search entry text changes.
        #[template_callback]
        fn on_signal_search_changed_search_entry(&self, _entry: &gtk::SearchEntry) {
            self.filter_tools();
        }

        /// Callback for when a tool is activated from the sidebar.
        #[template_callback]
        fn on_signal_row_activated_sidebar_listbox(&self, row: &gtk::ListBoxRow) {
            let tool_id = row.widget_name().to_string();
            self.load_and_show_tool(&tool_id);

            // Close sidebar on small screens
            if !self.toggle_sidebar_button.get().is_visible() {
                self.overlay_split_view.set_show_sidebar(false);
            }
        }

        /// Callback for when the "Toggle Sidebar" button is clicked.
        #[template_callback]
        fn on_signal_clicked_show_sidebar_button(button: &gtk::Button) {
            let window = button
                .ancestor(super::DevtoolboxWindow::static_type())
                .and_downcast::<super::DevtoolboxWindow>()
                .expect("Button should be inside DevtoolboxWindow");

            window.imp().overlay_split_view.set_show_sidebar(true);
        }

        /// Callback for when the "Mark Favorite" button is clicked.
        #[template_callback]
        fn on_signal_clicked_mark_favorite_button(&self) {
            let settings = Settings::new(APP_ID);
            let mut favorites = settings.strv("favorite-tools");

            // Get the current tool ID from the visible child in the stack
            let Some(tool_id) = self.content_view_stack.visible_child_name() else {
                return;
            };
            let tool_id = tool_id.as_str();

            if favorites.contains(tool_id) {
                // Remove from favorites
                let index = favorites.iter().position(|id| id == tool_id).unwrap();
                favorites.remove(index);
                settings.set_strv("favorite-tools", &favorites).unwrap();

                // Update button
                self.mark_favorite_button.set_icon_name("star-new");
                self.mark_favorite_button
                    .set_tooltip_text(Some(&gettext("Add to Favorites")));
            } else {
                // Add to favorites
                favorites.push(tool_id.into());
                settings.set_strv("favorite-tools", &favorites).unwrap();

                // Update button
                self.mark_favorite_button.set_icon_name("star-delete");
                self.mark_favorite_button
                    .set_tooltip_text(Some(&gettext("Remove from Favorites")));
            }

            self.refresh_favorite_menu();
        }

        /// Loads and displays the tool with the given ID in the content view stack.
        pub fn load_and_show_tool(&self, tool_id: &str) {
            let mut loaded_tools = self.loaded_tools.borrow_mut();

            // Check if the tool was already loaded
            if !loaded_tools.contains_key(tool_id) {
                // Find tool metadata
                if let Some(metadata) = all_tools().find(|t| t.id == tool_id) {
                    // Create tool view
                    let tool_view = self.create_tool_view(metadata);

                    // Add to stack
                    self.content_view_stack.add_named(&tool_view, Some(tool_id));

                    // Cache it
                    loaded_tools.insert(tool_id.to_string(), tool_view);
                }
            }

            // Update header bar title
            if let Some(metadata) = all_tools().find(|t| t.id == tool_id) {
                let title_widget = adw::WindowTitle::builder()
                    .title(&metadata.title)
                    .subtitle(&metadata.description)
                    .build();
                self.content_header_bar
                    .set_title_widget(Some(&title_widget));
            }

            // Update favorite button state
            let settings = Settings::new(APP_ID);
            if settings
                .strv("favorite-tools")
                .contains(&tool_id.to_string())
            {
                self.mark_favorite_button.set_icon_name("star-delete");
                self.mark_favorite_button
                    .set_tooltip_text(Some(&gettext("Remove from Favorites")));
            } else {
                self.mark_favorite_button.set_icon_name("star-new");
                self.mark_favorite_button
                    .set_tooltip_text(Some(&gettext("Add to Favorites")));
            }

            // Show the tool
            self.content_view_stack.set_visible_child_name(tool_id);

            // Select the corresponding row in the sidebar by name
            let mut i = 0;
            while let Some(row) = self.sidebar_listbox.row_at_index(i) {
                if row.widget_name() == tool_id {
                    self.sidebar_listbox.select_row(Some(&row));
                    break;
                }
                i += 1;
            }
        }

        /// Creates a new tool view widget based on the provided metadata.
        fn create_tool_view(&self, metadata: &'static ToolMetadata) -> gtk::Widget {
            let tool = match metadata.id {
                "config_format" => {
                    use crate::tools::config_format::ConfigFormatWidget;
                    ConfigFormatWidget::new().upcast()
                }
                "timestamp" => {
                    use crate::tools::timestamp::TimestampWidget;
                    TimestampWidget::new().upcast()
                }
                "number_bases" => {
                    use crate::tools::number_bases::NumberBasesWidget;
                    NumberBasesWidget::new().upcast()
                }
                "cron_parser" => {
                    use crate::tools::cron_parser::CronParserWidget;
                    CronParserWidget::new().upcast()
                }
                "cron_gen" => {
                    use crate::tools::cron_gen::CronGenWidget;
                    CronGenWidget::new().upcast()
                }
                "linux_permissions" => {
                    use crate::tools::linux_permissions::LinuxPermissionsWidget;
                    LinuxPermissionsWidget::new().upcast()
                }
                "html_enc" => {
                    use crate::tools::html_enc::HtmlEncWidget;
                    HtmlEncWidget::new().upcast()
                }
                "base64" => {
                    use crate::tools::base64::Base64Widget;
                    Base64Widget::new().upcast()
                }
                "url_enc" => {
                    use crate::tools::url_enc::UrlEncWidget;
                    UrlEncWidget::new().upcast()
                }
                "lipsum" => {
                    use crate::tools::lipsum::LipsumWidget;
                    LipsumWidget::new().upcast()
                }
                "uuid" => {
                    use crate::tools::uuid::UuidWidget;
                    UuidWidget::new().upcast()
                }
                "random" => {
                    use crate::tools::random::RandomWidget;
                    RandomWidget::new().upcast()
                }
                "text_inspector" => {
                    use crate::tools::text_inspector::TextInspectorWidget;
                    TextInspectorWidget::new().upcast()
                }
                "contrast_check" => {
                    use crate::tools::contrast_check::ContrastCheckWidget;
                    ContrastCheckWidget::new().upcast()
                }
                "color_spaces" => {
                    use crate::tools::color_spaces::ColorSpacesWidget;
                    ColorSpacesWidget::new().upcast()
                }
                "regex" => {
                    use crate::tools::regex::RegexWidget;
                    RegexWidget::new().upcast()
                }
                "qrcode" => {
                    use crate::tools::qrcode::QrcodeWidget;
                    QrcodeWidget::new().upcast()
                }
                "color_blindness" => {
                    use crate::tools::color_blindness::ColorBlindnessWidget;
                    ColorBlindnessWidget::new().upcast()
                }
                "text_diff" => {
                    use crate::tools::text_diff::TextDiffWidget;
                    TextDiffWidget::new().upcast()
                }
                "cert_parse" => {
                    use crate::tools::cert_parse::CertParseWidget;
                    CertParseWidget::new().upcast()
                }
                _ => {
                    panic!("Unknown tool ID: {}", metadata.id);
                }
            };

            tool
        }

        /// Creates a new ListBoxRow for the given tool metadata to be displayed
        /// in the sidebar or favorites list.
        fn create_tool_row(&self, tool: &'static ToolMetadata) -> gtk::ListBoxRow {
            let row_box = gtk::Box::new(gtk::Orientation::Horizontal, 4);
            row_box.set_margin_start(12);
            row_box.set_margin_end(12);
            row_box.set_margin_top(6);
            row_box.set_margin_bottom(6);
            row_box.set_spacing(12);

            let icon = gtk::Image::from_icon_name(tool.icon_name);
            row_box.append(&icon);

            let title = gtk::Label::new(None);
            if let Some(sidebar_title) = &tool.sidebar_title {
                title.set_label(sidebar_title);
            } else {
                title.set_label(&tool.title);
            }
            title.set_halign(gtk::Align::Start);
            title.add_css_class("body");
            row_box.append(&title);

            let row = gtk::ListBoxRow::new();
            row.set_widget_name(tool.id);
            row.set_child(Some(&row_box));
            row.set_tooltip_text(Some(&tool.description));

            row
        }

        /// Populates the sidebar with all available tools, grouped by category.
        fn populate_sidebar(&self) {
            for tool in all_tools() {
                self.sidebar_listbox.append(&self.create_tool_row(tool));
            }

            self.sidebar_listbox.set_header_func(|row, before| {
                let get_category = |r: &gtk::ListBoxRow| -> Option<String> {
                    let tool_id = r.widget_name();
                    all_tools()
                        .find(|t| t.id == tool_id)
                        .map(|t| t.category.category_title())
                };

                let current_category = get_category(row);
                let prev_category = before.and_then(get_category);

                if current_category != prev_category {
                    let header_label = gtk::Label::new(current_category.as_deref());
                    header_label.set_halign(gtk::Align::Start);
                    header_label.set_valign(gtk::Align::Center);
                    header_label.add_css_class("dimmed");
                    header_label.add_css_class("heading");
                    header_label.set_margin_start(12);
                    header_label.set_margin_bottom(6);

                    if before.is_some() {
                        header_label.set_margin_top(16);
                    }

                    row.set_header(Some(&header_label));
                }
            });
        }

        /// Refreshes the favorites menu based on the current list of favorite
        /// tools
        fn refresh_favorite_menu(&self) {
            self.favorite_listbox.remove_all();

            let settings = Settings::new(APP_ID);
            let favorite_tools = settings.strv("favorite-tools");

            if favorite_tools.is_empty() {
                self.favorite_view_stack.set_visible_child_name("empty");
            } else {
                for tool_id in favorite_tools {
                    if let Some(metadata) = all_tools().find(|t| t.id == tool_id) {
                        self.favorite_listbox
                            .append(&self.create_tool_row(metadata));
                    }
                }
                self.favorite_view_stack.set_visible_child_name("favorites");
            }
        }

        /// Sets up the GActions for the window
        fn setup_gactions(&self) {
            let obj = self.obj();

            let toggle_search = gio::ActionEntry::builder("toggle-search")
                .activate(|window: &super::DevtoolboxWindow, _, _| {
                    window.imp().toggle_search_action();
                })
                .build();

            let toggle_sidebar = gio::ActionEntry::builder("toggle-sidebar")
                .activate(|window: &super::DevtoolboxWindow, _, _| {
                    window.imp().toggle_sidebar_action();
                })
                .build();

            let shortcuts = gio::ActionEntry::builder("shortcuts")
                .activate(|window: &super::DevtoolboxWindow, _, _| {
                    window.imp().show_shortcuts_action();
                })
                .build();

            let open_menu = gio::ActionEntry::builder("open-menu")
                .activate(|window: &super::DevtoolboxWindow, _, _| {
                    window.imp().open_menu_action();
                })
                .build();

            obj.add_action_entries([toggle_search, toggle_sidebar, shortcuts, open_menu]);
        }

        /// Callback for the win.toggle-search action. Toggles the visibility of
        /// the search bar and focuses the search entry if activated.
        fn toggle_search_action(&self) {
            let is_active = !self.search_bar.is_search_mode();
            self.search_bar.set_search_mode(is_active);
            if is_active {
                self.search_entry.grab_focus();
                self.search_entry.select_region(0, -1);
            }
            self.show_search_button.set_active(is_active);
        }

        /// Callback for the win.toggle-sidebar action. Toggles the visibility of
        /// the sidebar and updates the toggle button state.
        fn toggle_sidebar_action(&self) {
            let is_open = !self.overlay_split_view.shows_sidebar();
            self.overlay_split_view.set_show_sidebar(is_open);
            self.toggle_sidebar_button.set_active(is_open);
        }

        /// Callback for the win.shortcuts action. Displays the shortcuts dialog.
        fn show_shortcuts_action(&self) {
            let shortcuts_dialog =
                gtk::Builder::from_resource("/me/iepure/devtoolbox/core/ui/shortcuts-dialog.ui")
                    .object::<adw::ShortcutsDialog>("shortcuts_dialog")
                    .unwrap();
            shortcuts_dialog.present(Some(&self.obj().clone().upcast::<gtk::Window>()));
        }

        /// Callback for the win.open-menu action. Opens the menu popover.
        fn open_menu_action(&self) {
            self.menu_button.popup();
        }

        /// Shows the search bar and sets the query in the search entry.
        pub fn show_search_with_query(&self, query: &str) {
            self.search_entry.set_text(query);
            self.search_bar.set_search_mode(true);
            self.search_entry.grab_focus();
        }

        /// Filters the tools in the sidebar based on the current text in the
        /// search entry.
        fn filter_tools(&self) {
            let search_text = self.search_entry.text().to_lowercase();

            // Restore sidebar if search text is empty
            if search_text.is_empty() {
                self.restore_sidebar();
                self.sidebar_view_stack.set_visible_child_name("all");
                return;
            }

            // Clear sidebar and rebuild with matching tools
            self.sidebar_listbox.remove_all();

            let matching_tools: Vec<_> = all_tools()
                .filter(|tool| {
                    tool.title.to_lowercase().contains(&search_text)
                        || tool.description.to_lowercase().contains(&search_text)
                        || tool.id.contains(&search_text)
                        || tool
                            .sidebar_title
                            .as_ref()
                            .map_or(false, |title| title.to_lowercase().contains(&search_text))
                        || tool
                            .keywords
                            .iter()
                            .any(|keyword| keyword.to_lowercase().contains(&search_text))
                })
                .collect();

            if matching_tools.is_empty() {
                self.sidebar_view_stack.set_visible_child_name("no-results");
                return;
            }

            for tool in &matching_tools {
                self.sidebar_listbox.append(&self.create_tool_row(tool));
            }

            // Select the currently visible tool in the sidebar
            if let Some(current_tool_id) = self.content_view_stack.visible_child_name() {
                let mut i = 0;
                while let Some(row) = self.sidebar_listbox.row_at_index(i) {
                    if row.widget_name() == current_tool_id {
                        self.sidebar_listbox.select_row(Some(&row));
                        break;
                    }
                    i += 1;
                }
            }

            self.sidebar_view_stack.set_visible_child_name("all");
        }

        /// Restores the sidebar to show all tools, grouped by category.
        fn restore_sidebar(&self) {
            self.sidebar_listbox.remove_all();
            for tool in all_tools() {
                self.sidebar_listbox.append(&self.create_tool_row(tool));
            }

            // Select the currently visible tool in the sidebar
            if let Some(current_tool_id) = self.content_view_stack.visible_child_name() {
                let mut i = 0;
                while let Some(row) = self.sidebar_listbox.row_at_index(i) {
                    if row.widget_name() == current_tool_id {
                        self.sidebar_listbox.select_row(Some(&row));
                        break;
                    }
                    i += 1;
                }
            }
        }
    }

    impl ObjectImpl for DevtoolboxWindow {
        fn constructed(&self) {
            self.parent_constructed();

            // Remove 'devel' CSS style if not in debug mode
            if !cfg!(debug_assertions) {
                self.obj().remove_css_class("devel");
            }

            // Populate content
            self.populate_sidebar();
            self.refresh_favorite_menu();

            // Show last used tool
            let settings = Settings::new(APP_ID);
            let last_tool_id = settings.string("last-tool");
            self.load_and_show_tool(&last_tool_id);

            // Search
            self.search_bar
                .set_key_capture_widget(Some(&self.obj().clone().upcast::<gtk::Widget>()));

            // Connect search button toggle to search bar visibility
            let obj_weak = self.obj().downgrade();
            self.show_search_button.connect_toggled(move |button| {
                let Some(obj) = obj_weak.upgrade() else {
                    return;
                };
                let imp = obj.imp();
                if *imp.updating_search_mode.borrow() {
                    return;
                }
                *imp.updating_search_mode.borrow_mut() = true;

                imp.search_bar.set_search_mode(button.is_active());
                if button.is_active() {
                    imp.search_entry.grab_focus();
                    imp.search_entry.select_region(0, -1);
                }

                *imp.updating_search_mode.borrow_mut() = false;
            });

            // Sync search bar mode to toggle button
            let obj_weak = self.obj().downgrade();
            self.search_bar
                .connect_search_mode_enabled_notify(move |_| {
                    let Some(obj) = obj_weak.upgrade() else {
                        return;
                    };
                    let imp = obj.imp();
                    if *imp.updating_search_mode.borrow() {
                        return;
                    }
                    *imp.updating_search_mode.borrow_mut() = true;
                    imp.show_search_button
                        .set_active(imp.search_bar.is_search_mode());
                    *imp.updating_search_mode.borrow_mut() = false;
                });

            // Register actions
            self.setup_gactions();

            // Set accelerators for actions
            let shortcut_controller = gtk::ShortcutController::new();
            shortcut_controller.set_scope(gtk::ShortcutScope::Managed);

            let accels: [(&str, &str); 4] = [
                ("<control>f", "win.toggle-search"),
                ("F9", "win.toggle-sidebar"),
                ("<control>question", "win.shortcuts"),
                ("F10", "win.open-menu"),
            ];

            for (accel, action_name) in accels {
                if let Some(trigger) = gtk::ShortcutTrigger::parse_string(accel) {
                    let action = gtk::NamedAction::new(action_name);
                    let shortcut = gtk::Shortcut::new(Some(trigger), Some(action));
                    shortcut_controller.add_shortcut(shortcut);
                }
            }
            self.obj().add_controller(shortcut_controller);

            // Bind settings
            settings
                .bind(
                    "window-width",
                    self.obj().upcast_ref::<gtk::Window>(),
                    "default-width",
                )
                .build();
            settings
                .bind(
                    "window-height",
                    self.obj().upcast_ref::<gtk::Window>(),
                    "default-height",
                )
                .build();
            settings
                .bind(
                    "window-maximized",
                    self.obj().upcast_ref::<gtk::Window>(),
                    "maximized",
                )
                .build();
            settings
                .bind("sidebar-open", &self.toggle_sidebar_button.get(), "active")
                .build();
            settings
                .bind(
                    "last-tool",
                    &self.content_view_stack.get(),
                    "visible-child-name",
                )
                .build();
        }
    }

    impl WidgetImpl for DevtoolboxWindow {}
    impl WindowImpl for DevtoolboxWindow {}
    impl ApplicationWindowImpl for DevtoolboxWindow {}
    impl AdwApplicationWindowImpl for DevtoolboxWindow {}
}

glib::wrapper! {
    pub struct DevtoolboxWindow(ObjectSubclass<imp::DevtoolboxWindow>)
        @extends gtk::Widget, gtk::Window, gtk::ApplicationWindow, adw::ApplicationWindow,
                 gtk::Native, gtk::Root, gtk::ShortcutManager,
        @implements gio::ActionGroup, gio::ActionMap, gtk::ConstraintTarget, gtk::Buildable, gtk::Accessible;
}

impl DevtoolboxWindow {
    pub fn new<P: IsA<gtk::Application>>(application: &P) -> Self {
        glib::Object::builder()
            .property("application", application)
            .build()
    }

    pub fn show_tool(&self, tool_id: &str) {
        self.imp().load_and_show_tool(tool_id);
    }

    pub fn search_tools(&self, query: &str) {
        self.imp().show_search_with_query(query);
    }
}
