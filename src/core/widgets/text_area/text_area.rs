/*
 * text_area.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gettextrs::{gettext, pgettext};
use gtk::prelude::*;
use gtk::{gdk, gio, glib, glib::subclass::Signal, glib::Properties, CompositeTemplate};
use sourceview::prelude::*;

use std::cell::RefCell;

use std::{fmt::Debug, sync::OnceLock};

use crate::core::widgets::text_area::wrap_mode::WrapMode;

// MARK: Implementation
mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/core/widgets/text_area/text_area.ui")]
    #[properties(wrapper_type = super::TextArea, )]
    pub struct TextArea {
        // MARK: Template widgets
        #[template_child]
        view_stack: TemplateChild<adw::ViewStack>,

        #[template_child]
        drop_revealer: TemplateChild<gtk::Revealer>,

        #[template_child]
        source_view: TemplateChild<sourceview::View>,

        #[template_child]
        open_button: TemplateChild<gtk::Button>,

        #[template_child]
        open_file_dialog: TemplateChild<gtk::FileDialog>,

        // MARK: Properties
        /// The title of the text area
        #[property(set, get, type = String)]
        title: RefCell<String>,

        /// Whether the text area is in a working state. When true, a spinner is shown in the header.
        #[property(set, get, type = bool, default = false)]
        working: RefCell<bool>,

        /// Visibility of the action button. When false, the button is hidden. Control the button's label with the property
        /// 'action-button-label'.
        #[property(set, get, type = bool, default = false)]
        action_button_visible: RefCell<bool>,

        /// Visibility of the open button. When false, the button is hidden. The open button opens a GtkFileDialog to load
        /// a file into the text area. The contents of the file is treated as plain text. Use the property 'file-extensions'
        /// to filter the files shown in the dialog.
        #[property(set, get, type = bool, default = false)]
        open_button_visible: RefCell<bool>,

        /// Visibility of the copy button. When false, the button is hidden. The copy button copies the contents of the text area
        /// to the clipboard.
        #[property(set, get, type = bool, default = false)]
        copy_button_visible: RefCell<bool>,

        /// Visibility of the paste button. When false, the button is hidden. The paste button pastes the contents of the clipboard
        /// into the text area. Only plain text is pasted into the text area. Text already present in the text area is replaced.
        #[property(set, get, type = bool, default = false)]
        paste_button_visible: RefCell<bool>,

        /// Visibility of the clear button. When false, the button is hidden. The clear button clears the contents of the text area.
        #[property(set, get, type = bool, default = false)]
        clear_button_visible: RefCell<bool>,

        /// Whether the text area is editable. When false, the text area is read-only to the user.
        #[property(set, get, type = bool, default = true)]
        editable: RefCell<bool>,

        /// Show line numbers in the text area. When true, line numbers are shown in the margin of the text area.
        #[property(set, get, type = bool, default = false)]
        show_line_numbers: RefCell<bool>,

        /// Highlight the current line in the text area. When true, the line where the cursor is located is highlighted.
        #[property(set, get, type = bool, default = false)]
        highlight_current_line: RefCell<bool>,

        /// Enable syntax highlighting in the text area. When true, syntax highlighting is enabled based on the language
        /// specified in the 'language' property.
        #[property(set, get, type = bool, default = false)]
        highlight_syntax: RefCell<bool>,

        /// The programming language for syntax highlighting. Must be a valid language ID from SourceView. When empty, no
        /// language is set. To be used only if 'highlight-syntax' is true.
        #[property(set, get, type = String, default = "")]
        language: RefCell<String>,

        /// Use a monospace font in the text area. When true, the text area uses a monospace font.
        #[property(set, get, type = bool, default = false)]
        monospace: RefCell<bool>,

        /// The height of the text area in pixels. Default is 200.
        #[property(set, get, type = u32, default = 200)]
        height: RefCell<u32>,

        /// Add a filter for text files in the open file dialog. When true, the file dialog will add a filter
        /// for text files. By default, a file dialog shows all file types.
        #[property(set, get, type = bool, default = true)]
        filter_text_files: RefCell<bool>,

        /// Add a filter for the file extensions specified in the 'filter-custom-file-extensions' property. The name is set to "Supported
        /// file types", translated in the current locale. When true, the file dialog will add a filter for the file
        /// extensions specified in the 'filter-custom-file-extensions' property. By default, a file dialog shows all file types.
        #[property(set, get, type = bool, default = false)]
        filter_custom_files: RefCell<bool>,

        /// Custom file extensions for the open file dialog. A comma-separated list of file extensions (e.g. "json,yaml,xml").
        /// Only used if 'filter-custom-files' is true.
        #[property(set, get, type = glib::StrV)]
        filter_custom_file_extensions: RefCell<Vec<String>>,

        /// The label of the action button. When empty, the button will have no label. Useful only if 'action-button-visible'
        /// is true.
        #[property(set, get, type = String, default = "")]
        action_button_label: RefCell<String>,

        /// The label shown when loading a file. Useful when opening large files that may take some time to load. Defaults
        /// to "Loading..." in the current locale.
        #[property(set, get, type = String)]
        loading_label: RefCell<String>,

        /// Allow drag and drop of files into the text area. When true, files can be dragged and dropped into the text area
        /// to load their contents as plain text.
        #[property(set, get, type = bool, default = false)]
        allow_drag_and_drop: RefCell<bool>,

        /// Whether a file is being dragged over the text area. Used for styling the drop target.
        #[property(set, get, type = bool, default = false)]
        dragging: RefCell<bool>,

        /// Error state of the text area. When true, the text area is highlighted to indicate an error and an error icon
        /// is shown in the header. Hovering over the icon shows more information about the error.
        #[property(set, get, type = bool, default = false)]
        error: RefCell<bool>,

        /// Error label shown as tooltip when hovering over the error icon. Useful only if 'error' is true.
        #[property(set, get, type = String, default = "")]
        error_label: RefCell<String>,

        /// Wrap mode of the text area. Accepts: "none", "char", "word", "word-char"
        #[property(set, get, type = String, default = "none")]
        wrap_mode: RefCell<String>,

        // MARK: Other fields
        text_changed_handler_id: RefCell<Option<glib::SignalHandlerId>>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for TextArea {
        const NAME: &'static str = "TextArea";
        type Type = super::TextArea;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
            klass.set_css_name("text-area");
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl TextArea {
        // MARK: Signal handlers
        /// Action button clicked. Emits the "action-clicked" signal.
        #[template_callback]
        fn on_signal_clicked_action_button(&self, _button: &gtk::Button) {
            self.obj().emit_by_name::<()>("action-clicked", &[]);
        }

        /// Copy button clicked. Copies the contents of the text area to the clipboard.
        #[template_callback]
        fn on_signal_clicked_copy_button(&self, _button: &gtk::Button) {
            let text_buffer = self.source_view.buffer();
            let text = text_buffer.text(&text_buffer.start_iter(), &text_buffer.end_iter(), false);
            let clipboard = self.source_view.clipboard();
            clipboard.set_text(&text);
        }

        /// Paste button clicked. Pastes the contents of the clipboard into the text area at the end of the currently
        /// existing text.
        #[template_callback]
        fn on_signal_clicked_paste_button(&self, _button: &gtk::Button) {
            let clipboard = self.source_view.clipboard();
            let buffer = self.source_view.buffer();
            buffer.paste_clipboard(&clipboard, Some(&buffer.end_iter()), true);
        }

        /// Clear button clicked. Clears the text area and emits the "cleared" signal.
        #[template_callback]
        fn on_signal_clicked_clear_button(&self, _button: &gtk::Button) {
            self.clear();
            self.obj().emit_by_name::<()>("cleared", &[]);
        }

        /// Open button clicked. Opens a file dialog to select a file to load into the text area.
        #[template_callback]
        async fn on_signal_clicked_open_button(&self, _button: &gtk::Button) {
            self.open_button.set_sensitive(false);

            let filter_store = gio::ListStore::new::<gtk::FileFilter>();

            // Text files
            if self.obj().filter_text_files() {
                let text_filter = gtk::FileFilter::new();
                text_filter.set_name(Some(&pgettext("File filter", "Text Files")));
                text_filter.add_mime_type("text/*");
                filter_store.append(&text_filter);
            }

            // Custom file extensions
            if self.obj().filter_custom_files() {
                let custom_filter = gtk::FileFilter::new();
                custom_filter.set_name(Some(&pgettext("File filter", "Supported File Types")));
                for ext in self.obj().filter_custom_file_extensions() {
                    let suffix = format!("*.{}", ext.trim().trim_start_matches('.'));
                    custom_filter.add_suffix(&suffix);
                }
                filter_store.append(&custom_filter);
            }

            // Default all files filter
            let all_files_filter = gtk::FileFilter::new();
            all_files_filter.set_name(Some(&pgettext("File filter", "All Files")));
            all_files_filter.add_pattern("*");
            filter_store.append(&all_files_filter);

            self.open_file_dialog.set_filters(Some(&filter_store));

            // Show dialog to user
            let result = self
                .open_file_dialog
                .open_future(Some(
                    &self.obj().root().and_downcast::<gtk::Window>().unwrap(),
                ))
                .await;

            // Handle result
            match result {
                Ok(file) => {
                    self.read_file_into_text_area(&file).await;
                }
                Err(err) => {
                    // Translator: {message} is replaced with the error message
                    let tmpl = pgettext("Error message", "Unable to open file: {message}");
                    let msg = tmpl.replace("{message}", &err.message());
                    self.obj().emit_by_name::<()>("error", &[&msg]);
                }
            }
            self.open_button.set_sensitive(true);
        }

        // MARK: Helpers
        /// Set theme for the source view. If the application is in dark mode, the "Adwaita-dark" style scheme is used,
        /// otherwise the "Adwaita" style scheme is used. Called on construction and when the theme changes.
        fn set_theme(&self) {
            let style_scheme = if adw::StyleManager::default().is_dark() {
                sourceview::StyleSchemeManager::default().scheme("Adwaita-dark")
            } else {
                sourceview::StyleSchemeManager::default().scheme("Adwaita")
            };
            if let Some(scheme) = style_scheme {
                if let Some(source_buffer) = self
                    .source_view
                    .buffer()
                    .downcast_ref::<sourceview::Buffer>()
                {
                    source_buffer.set_style_scheme(Some(&scheme));
                }
            }
        }

        /// Clear the text area. Called when the clear button is clicked.
        pub fn clear(&self) {
            if let Some(source_buffer) = self
                .source_view
                .buffer()
                .downcast_ref::<sourceview::Buffer>()
            {
                source_buffer.set_text("");
            }
            self.source_view.remove_css_class("error-highlight");
            self.view_stack.set_visible_child_name("text-area");
            self.obj().set_working(false);
        }

        /// Read the contents of a file into the text area. Called when a file is selected in the open file dialog or
        /// dropped into the text area.
        async fn read_file_into_text_area(&self, file: &gio::File) {
            self.view_stack.set_visible_child_name("loading");

            let result: Result<(glib::Slice<u8>, Option<glib::GString>), glib::Error> =
                file.load_contents_future().await;

            match result {
                Ok((data, _tags)) => {
                    if data.len() > 0 {
                        if let Some(source_buffer) = self
                            .source_view
                            .buffer()
                            .downcast_ref::<sourceview::Buffer>()
                        {
                            let text = String::from_utf8(data.to_vec());
                            match text {
                                Ok(text) => {
                                    source_buffer.set_text(&text);
                                }
                                Err(_) => {
                                    self.obj().emit_by_name::<()>(
                                        "error",
                                        &[&pgettext(
                                            "Error message",
                                            "The file does not contain plain text",
                                        )],
                                    );
                                }
                            }
                        }
                    } else {
                        self.obj().emit_by_name::<()>(
                            "error",
                            &[&pgettext("Error message", "The file is empty.")],
                        );
                    }
                }
                Err(err) => {
                    // Translator: {message} is replaced with the error message
                    let tmpl = pgettext("Error message", "Unable to read file: {message}");
                    let msg = tmpl.replace("{message}", &err.to_string());
                    self.obj().emit_by_name::<()>("error", &[&msg]);
                }
            }
            self.view_stack.set_visible_child_name("text-area");
        }

        pub fn text(&self) -> String {
            self.source_view
                .buffer()
                .text(
                    &self.source_view.buffer().start_iter(),
                    &self.source_view.buffer().end_iter(),
                    false,
                )
                .to_string()
        }

        pub fn set_text(&self, text: String) {
            if let Some(source_buffer) = self
                .source_view
                .buffer()
                .downcast_ref::<sourceview::Buffer>()
            {
                source_buffer.set_text(&text);
            }
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for TextArea {
        // MARK: Construction
        fn constructed(&self) {
            self.parent_constructed();

            // Set default loading label
            if self.loading_label.borrow().is_empty() {
                self.obj().set_loading_label(gettext("Loading..."));
            }

            // Set theme
            self.set_theme();

            // Set language if specified
            let obj = self.obj().clone();
            let obj_clone = obj.clone();
            obj.connect_notify_local(Some("language"), move |_text_area, _param_spec| {
                if let Some(imp) = obj_clone.downcast_ref::<super::TextArea>() {
                    let language = sourceview::LanguageManager::default()
                        .language(&imp.imp().language.borrow());
                    if let Some(source_buffer) = imp
                        .imp()
                        .source_view
                        .buffer()
                        .downcast_ref::<sourceview::Buffer>()
                    {
                        source_buffer.set_language(language.as_ref());
                    }
                }
            });

            // Bind properties to the source view (rest are bound in the template)
            self.obj()
                .bind_property(
                    "highlight-syntax",
                    &self.source_view.buffer(),
                    "highlight-syntax",
                )
                .build();
            self.obj()
                .bind_property(
                    "highlight-syntax",
                    &self.source_view.buffer(),
                    "highlight-matching-brackets",
                )
                .build();

            // Connect signals (rest are connected in the template)
            // Text changed
            let obj = self.obj().clone();
            *self.text_changed_handler_id.borrow_mut() =
                Some(self.source_view.buffer().connect_changed(move |_buffer| {
                    obj.emit_by_name::<()>("changed", &[]);
                }));

            // Theme changed
            let obj = self.obj().clone();
            adw::StyleManager::default().connect_notify_local(
                Some("dark"),
                move |_style_manager, _param_spec| {
                    if let Some(text_area) = obj.downcast_ref::<super::TextArea>() {
                        text_area.imp().set_theme();
                    }
                },
            );

            // Error state
            let obj = self.obj().clone();
            obj.connect_notify_local(Some("error"), move |text_area, _param_spec| {
                if text_area.error() {
                    text_area.imp().source_view.add_css_class("error-highlight");
                } else {
                    text_area
                        .imp()
                        .source_view
                        .remove_css_class("error-highlight");
                }
            });

            // Wrap mode
            let obj = self.obj().clone();
            obj.connect_notify_local(Some("wrap-mode"), move |text_area, _param_spec| {
                let wrap_mode_str = text_area.wrap_mode();
                let wrap_mode_enum = WrapMode::from(wrap_mode_str.as_str());
                let gtk_wrap_mode = gtk::WrapMode::from(wrap_mode_enum);
                text_area.imp().source_view.set_wrap_mode(gtk_wrap_mode);
            });

            // Drag and drop
            let drop_target =
                gtk::DropTarget::new(gdk::FileList::static_type(), gdk::DragAction::COPY);

            let obj = self.obj().clone();
            let imp = self.obj().downgrade();
            drop_target.connect_drop(move |_, value, _, _| {
                // Reject drop if drag and drop is not allowed
                if !obj.allow_drag_and_drop() {
                    return false;
                }

                let files = value
                    .get::<gdk::FileList>()
                    .expect("Failed to get FileList from drop value");
                if files.files().len() != 1 {
                    obj.emit_by_name::<()>(
                        "error",
                        &[&pgettext(
                            "Error message",
                            "Only one file can be opened at a time.",
                        )],
                    );
                    obj.set_working(false);
                    return false;
                }

                if let Some(text_area) = imp.upgrade() {
                    glib::spawn_future_local(async move {
                        text_area
                            .imp()
                            .read_file_into_text_area(&files.files()[0])
                            .await;
                    });
                }
                obj.imp().view_stack.set_visible_child_name("text-area");
                true
            });
            self.source_view.add_controller(drop_target);
        }

        // MARK: Signals
        fn signals() -> &'static [Signal] {
            static SIGNALS: OnceLock<Vec<Signal>> = OnceLock::new();
            SIGNALS.get_or_init(|| {
                vec![
                    Signal::builder("changed").build(),
                    Signal::builder("action-clicked").build(),
                    Signal::builder("error")
                        .param_types([String::static_type()])
                        .build(),
                    Signal::builder("cleared").build(),
                ]
            })
        }
    }

    impl WidgetImpl for TextArea {}
    impl BinImpl for TextArea {}
}

// MARK: Wrapper
glib::wrapper! {
    pub struct TextArea(ObjectSubclass<imp::TextArea>)
        @extends adw::Bin, gtk::Widget,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

// MARK: Widget
impl TextArea {
    pub fn new(title: &str) -> Self {
        glib::Object::builder()
            .property("title", title)
            .property("loading-label", gettext("Loading..."))
            .build()
    }

    pub fn clear(&self) {
        self.imp().clear();
    }

    pub fn text(&self) -> String {
        self.imp().text()
    }

    pub fn set_text(&self, text: String) {
        self.imp().set_text(text);
    }

    // pub fn set_error(&self, error: bool) {
    //     self.imp().set_error(error);
    // }
}
