/* window.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gio, glib, CompositeTemplate};

mod imp {
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
        sidebar_listbox: TemplateChild<gtk::ListBox>,

        #[template_child]
        mark_favorite_button: TemplateChild<gtk::Button>,

        #[template_child]
        content_view_stack: TemplateChild<adw::ViewStack>,

        // Other fields
        loaded_tools: RefCell<HashMap<String, gtk::Widget>>,
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
        #[template_callback]
        fn on_signal_map(&self) {
            self.sidebar_listbox.grab_focus();
            self.content_view_stack
                .visible_child()
                .unwrap()
                .grab_focus();
        }

        #[template_callback]
        fn on_signal_row_activated_favorite_listbox(&self, _row: &gtk::ListBoxRow) {
            // TODO: implement favorite tool activation
        }

        #[template_callback]
        fn on_signal_search_changed_search_entry(_entry: &gtk::SearchEntry) {
            // TODO: implement tool search filtering
        }

        #[template_callback]
        fn on_signal_row_activated_sidebar_listbox(&self, row: &gtk::ListBoxRow) {
            let tool_id = row.widget_name().to_string();
            self.load_and_show_tool(&tool_id);

            // Close sidebar on small screens
            if !self.toggle_sidebar_button.get().is_visible() {
                self.overlay_split_view.set_show_sidebar(false);
            }
        }

        #[template_callback]
        fn on_signal_clicked_show_sidebar_button(button: &gtk::Button) {
            let window = button
                .ancestor(super::DevtoolboxWindow::static_type())
                .and_downcast::<super::DevtoolboxWindow>()
                .expect("Button should be inside DevtoolboxWindow");

            window.imp().overlay_split_view.set_show_sidebar(true);
        }

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
        }

        fn load_and_show_tool(&self, tool_id: &str) {
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

            // Select the corresponding row in the sidebar
            if let Some(index) = all_tools().position(|tool_metadata| tool_metadata.id == tool_id) {
                if let Some(row) = self.sidebar_listbox.row_at_index(index as i32) {
                    self.sidebar_listbox.select_row(Some(&row));
                }
            }
        }

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
                _ => {
                    panic!("Unknown tool ID: {}", metadata.id);
                }
            };

            tool
        }

        fn populate_sidebar(&self) {
            for tool in all_tools() {
                let row_box = gtk::Box::new(gtk::Orientation::Horizontal, 4);
                row_box.set_margin_start(12);
                row_box.set_margin_end(12);
                row_box.set_margin_top(6);
                row_box.set_margin_bottom(6);
                row_box.set_spacing(12);

                let icon = gtk::Image::from_icon_name(tool.id);
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
                self.sidebar_listbox.append(&row);
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
    }

    impl ObjectImpl for DevtoolboxWindow {
        fn constructed(&self) {
            self.parent_constructed();

            // Populate sidebar
            self.populate_sidebar();

            // Show last used tool
            let settings = Settings::new(APP_ID);
            let last_tool_id = settings.string("last-tool");
            self.load_and_show_tool(&last_tool_id);

            // TODO: remove 'devel' css class if not in debug mode
            // TODO: figure out why shortcut dialog is disabled

            // Bind settings
            let settings = Settings::new(APP_ID);
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
}
