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

use std::cell::RefCell;

use std::{fmt::Debug, sync::OnceLock};

// MARK: Implementation
mod imp {
    use gtk::FileLauncher;

    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/devtoolbox/core/widgets/image_area/image_area.ui")]
    #[properties(wrapper_type = super::ImageArea, )]
    pub struct ImageArea {
        // MARK: Template widgets
        #[template_child]
        view_stack: TemplateChild<adw::ViewStack>,

        #[template_child]
        source_scrolled_window: TemplateChild<gtk::ScrolledWindow>,

        #[template_child]
        drop_revealer: TemplateChild<gtk::Revealer>,

        #[template_child]
        picture: TemplateChild<gtk::Picture>,

        #[template_child]
        open_button: TemplateChild<gtk::Button>,

        #[template_child]
        open_file_dialog: TemplateChild<gtk::FileDialog>,

        #[template_child]
        save_button: TemplateChild<gtk::Button>,

        #[template_child]
        save_file_dialog: TemplateChild<gtk::FileDialog>,

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
        /// an image into the Picture widget. Use the property 'file-extensions' to filter the files shown in the dialog.
        #[property(set, get, type = bool, default = false)]
        open_button_visible: RefCell<bool>,

        /// Visibility of the save button. When false, the button is hidden. The save button opens a GtkFileDialog to save
        /// the contents of the Picture widget to a file. Use the property 'file-extensions' to filter the files shown in the dialog.
        #[property(set, get, type = bool, default = false)]
        save_button_visible: RefCell<bool>,

        /// Visibility of the view button. When false, the button is hidden. The view button opens the image in an external
        /// application. Relies on the OpenURI portal.
        #[property(set, get, type = bool, default = false)]
        view_button_visible: RefCell<bool>,

        /// Visibility of the clear button. When false, the button is hidden. The clear button clears the contents of the text area.
        #[property(set, get, type = bool, default = false)]
        clear_button_visible: RefCell<bool>,

        /// The height of the Picture widget in pixels. Default is 200.
        #[property(set, get, type = u32, default = 200)]
        height: RefCell<u32>,

        /// Add a filter for image files in the open file dialog. When true, the file dialog will add a filter
        /// for image files. By default, a file dialog shows all file types.
        #[property(set, get, type = bool, default = true)]
        filter_image_files: RefCell<bool>,

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

        /// Allow drag and drop of files into the text area. When true, files can be dragged and dropped into the text area
        /// to load their contents as plain text.
        #[property(set, get, type = bool, default = false)]
        allow_drag_and_drop: RefCell<bool>,

        /// Whether a file is being dragged over the image area. Used for styling the drop target.
        #[property(set, get, type = bool, default = false)]
        dragging: RefCell<bool>,

        /// Error state of the image area. When true, the image area is highlighted to indicate an error and an error icon
        /// is shown in the header. Hovering over the icon shows more information about the error.
        #[property(set, get, type = bool, default = false)]
        error: RefCell<bool>,

        /// Error label shown as tooltip when hovering over the error icon. Useful only if 'error' is true.
        #[property(set, get, type = String, default = "")]
        error_label: RefCell<String>,

        /// Default filename used in the save file dialog when saving the contents of the image area.
        #[property(set, get, type = String)]
        default_save_filename: RefCell<String>,

        /// The label shown when loading a file. Useful when opening large files that may take some time to load. Defaults
        /// to "Loading..." in the current locale.
        #[property(set, get, type = String)]
        loading_label: RefCell<String>,

        /// The source file currently shown in the image area.
        /// Setting this property loads the image with glycin and updates the Picture texture.
        /// Setting it to `None` clears the current image.
        #[property(set, get, nullable, type = gio::File)]
        file: RefCell<Option<gio::File>>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for ImageArea {
        const NAME: &'static str = "ImageArea";
        type Type = super::ImageArea;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            klass.bind_template_callbacks();
            klass.set_css_name("image-area");
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    #[gtk::template_callbacks]
    impl ImageArea {
        fn update_vertical_expand(&self) {
            let should_expand = self.obj().valign() == gtk::Align::Fill;
            self.view_stack.set_vexpand(should_expand);
            self.source_scrolled_window.set_vexpand(should_expand);
        }

        // MARK: Signal handlers
        /// Action button clicked. Emits the "action-clicked" signal.
        #[template_callback]
        fn on_signal_clicked_action_button(&self, _button: &gtk::Button) {
            self.obj().emit_by_name::<()>("action-clicked", &[]);
        }

        /// Clear button clicked. Clears the image area and emits the "cleared" signal.
        #[template_callback]
        fn on_signal_clicked_clear_button(&self, _button: &gtk::Button) {
            self.obj().set_file(Option::<&gio::File>::None);
            self.obj().emit_by_name::<()>("cleared", &[]);
        }

        /// Open button clicked. Opens a file dialog to select a file to load into the image area.
        #[template_callback]
        async fn on_signal_clicked_open_button(&self, _button: &gtk::Button) {
            self.open_button.set_sensitive(false);

            let filter_store = gio::ListStore::new::<gtk::FileFilter>();

            // Image files
            if self.obj().filter_image_files() {
                let image_filter = gtk::FileFilter::new();
                image_filter.set_name(Some(&pgettext("File filter", "Image Files")));

                for mime_type in glycin::Loader::supported_mime_types().await {
                    image_filter.add_mime_type(mime_type.as_str());
                }

                filter_store.append(&image_filter);
            }

            // Custom file extensions
            if self.obj().filter_custom_files() {
                let custom_filter = gtk::FileFilter::new();
                custom_filter.set_name(Some(&pgettext("File filter", "Supported File Types")));

                for ext_list in self.obj().filter_custom_file_extensions() {
                    for ext in ext_list.split(',') {
                        custom_filter.add_suffix(&ext.trim().trim_start_matches('.'));
                    }
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
                    self.obj().set_file(Some(file));
                }
                Err(err) => {
                    // Ignore user dismissals: canceling the dialog is an expected interaction.
                    let dismissed =
                        err.kind::<gtk::DialogError>() == Some(gtk::DialogError::Dismissed);
                    if !dismissed {
                        // Translator: {message} is replaced with the error message
                        let tmpl = pgettext("Error message", "Unable to open file: {message}");
                        let msg = tmpl.replace("{message}", &err.message());
                        self.obj().emit_by_name::<()>("error", &[&msg]);
                    }
                }
            }
            self.open_button.set_sensitive(true);
        }

        /// Limitation: only PNGs are supported for saving
        #[template_callback]
        async fn on_signal_clicked_save_button(&self, _button: &gtk::Button) {
            self.save_button.set_sensitive(false);

            // Error on no image
            let Some(paintable) = self.picture.paintable() else {
                self.obj().emit_by_name::<()>(
                    "error",
                    &[&pgettext("Error message", "There is no image to save.")],
                );
                self.save_button.set_sensitive(true);
                return;
            };

            // Error if paintable is not a texture
            let Ok(texture) = paintable.downcast::<gdk::Texture>() else {
                self.obj().emit_by_name::<()>(
                    "error",
                    &[&pgettext(
                        "Error message",
                        "Unable to export the current image.",
                    )],
                );
                self.save_button.set_sensitive(true);
                return;
            };

            // Set default filename if available
            if !self.default_save_filename.borrow().is_empty() {
                self.save_file_dialog
                    .set_initial_name(Some(&self.obj().default_save_filename()));
            }

            // Show dialog to user
            let result = self
                .save_file_dialog
                .save_future(Some(
                    &self.obj().root().and_downcast::<gtk::Window>().unwrap(),
                ))
                .await;

            match result {
                Ok(file) => {
                    // Error if no path is provided
                    let Some(path) = file.path() else {
                        self.obj().emit_by_name::<()>(
                            "error",
                            &[&pgettext(
                                "Error message",
                                "Saving to non-local locations is not supported.",
                            )],
                        );
                        self.save_button.set_sensitive(true);
                        return;
                    };

                    // Save texture to file
                    if let Err(err) = texture.save_to_png(&path) {
                        // Translator: {message} is replaced with the error message
                        let tmpl = pgettext("Error message", "Unable to save file: {message}");
                        let msg = tmpl.replace("{message}", &err.to_string());
                        self.obj().emit_by_name::<()>("error", &[&msg]);
                        self.save_button.set_sensitive(true);
                        return;
                    }

                    // Emit signal with save path as parameter
                    self.obj()
                        .emit_by_name::<()>("image-saved", &[&path.display().to_string()]);
                }
                Err(err) => {
                    // Ignore user dismissals: canceling the dialog is an expected interaction.
                    let dismissed =
                        err.kind::<gtk::DialogError>() == Some(gtk::DialogError::Dismissed);
                    if !dismissed {
                        // Translator: {message} is replaced with the error message
                        let tmpl = pgettext("Error message", "Unable to save file: {message}");
                        let msg = tmpl.replace("{message}", &err.message());
                        self.obj().emit_by_name::<()>("error", &[&msg]);
                    }
                }
            }
            self.save_button.set_sensitive(true);
        }

        #[template_callback]
        fn on_signal_clicked_view_button(&self, _button: &gtk::Button) {
            // Error on no image
            let Some(_paintable) = self.picture.paintable() else {
                self.obj().emit_by_name::<()>(
                    "error",
                    &[&pgettext(
                        "Error message",
                        "There is no image to show in another program.",
                    )],
                );
                self.save_button.set_sensitive(true);
                return;
            };

            let file = match self.file.borrow().clone() {
                Some(file) => file,
                None => return,
            };

            // Allow consumers to intercept the request and suppress the default launcher.
            if self.obj().emit_by_name::<bool>("view-requested", &[&file]) {
                return;
            }

            let parent = self.obj().root().and_downcast::<gtk::Window>();
            let image_area = self.obj().downgrade();
            glib::spawn_future_local(async move {
                let launcher = FileLauncher::new(Some(&file));
                if let Err(err) = launcher.launch_future(parent.as_ref()).await {
                    if let Some(image_area) = image_area.upgrade() {
                        // Translator: {message} is replaced with the error message
                        let tmpl = pgettext("Error message", "Unable to open file: {message}");
                        let msg = tmpl.replace("{message}", &err.message());
                        image_area.emit_by_name::<()>("error", &[&msg]);
                    }
                }
            });
        }

        // MARK: Helpers
        /// Clear the text area. Called when the clear button is clicked.
        pub fn clear(&self) {
            self.picture.set_paintable(Option::<&gdk::Texture>::None);
            self.view_stack.set_visible_child_name("image-area");
            self.picture.remove_css_class("error-highlight");
            self.obj().set_working(false);
            self.obj().set_error(false);
        }

        /// Read the contents of a file into the Picture widget. Called when a file is selected in the open file dialog or
        /// dropped into the image area.
        async fn read_file_into_image_area(&self, file: &gio::File) {
            self.view_stack.set_visible_child_name("loading");

            let result = glycin::Loader::new(file.clone()).load().await;
            match result {
                Ok(image) => {
                    let texture = image.next_frame().await;
                    match texture {
                        Ok(frame) => {
                            self.obj().set_error(false);
                            self.obj().emit_by_name::<()>("image-loaded", &[]);
                            self.picture.set_paintable(Some(&frame.texture()));
                        }
                        Err(err) => {
                            // Translator: {message} is replaced with the error message
                            let tmpl = pgettext("Error message", "Unable to load image: {message}");
                            let msg = tmpl.replace("{message}", &err.to_string());
                            self.obj().emit_by_name::<()>("error", &[&msg]);
                            self.obj().set_error(true);
                        }
                    }
                }
                Err(err) => {
                    // Translator: {message} is replaced with the error message
                    let tmpl = pgettext("Error message", "Unable to load file: {message}");
                    let msg = tmpl.replace("{message}", &err.to_string());
                    self.obj().emit_by_name::<()>("error", &[&msg]);
                    self.obj().set_error(true);
                }
            }

            self.view_stack.set_visible_child_name("image-area");
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for ImageArea {
        // MARK: Construction
        fn constructed(&self) {
            self.parent_constructed();

            self.update_vertical_expand();

            let obj = self.obj().clone();
            obj.connect_notify_local(Some("valign"), move |image_area, _param_spec| {
                image_area.imp().update_vertical_expand();
            });

            // Set default filename for save file dialog
            if self.default_save_filename.borrow().is_empty() {
                self.obj()
                    .set_default_save_filename(gettext("Untitled Image"));
            }

            // Set default loading label
            if self.loading_label.borrow().is_empty() {
                self.obj().set_loading_label(gettext("Loading..."));
            }

            // Error state
            let obj = self.obj().clone();
            obj.connect_notify_local(Some("error"), move |image_area, _param_spec| {
                if image_area.error() {
                    image_area.imp().picture.add_css_class("error-highlight");
                } else {
                    image_area.imp().picture.remove_css_class("error-highlight");
                }
            });

            // File changes
            let obj = self.obj().clone();
            obj.connect_notify_local(Some("file"), move |image_area, _param_spec| {
                let file = image_area.imp().file.borrow().clone();
                let Some(file) = file else {
                    image_area.imp().clear();
                    return;
                };

                let image_area = image_area.downgrade();
                glib::spawn_future_local(async move {
                    if let Some(image_area) = image_area.upgrade() {
                        image_area.imp().read_file_into_image_area(&file).await;
                    }
                });
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

                if let Some(image_area) = imp.upgrade() {
                    image_area.set_file(Some(files.files()[0].clone()));
                }
                obj.imp().view_stack.set_visible_child_name("image-area");
                true
            });
            self.picture.add_controller(drop_target);
        }

        // MARK: Signals
        fn signals() -> &'static [Signal] {
            static SIGNALS: OnceLock<Vec<Signal>> = OnceLock::new();
            SIGNALS.get_or_init(|| {
                vec![
                    // Emitted when the action button is clicked.
                    Signal::builder("action-clicked").build(),
                    // Emitted when an error occurs. The error message is passed as a parameter.
                    Signal::builder("error")
                        .param_types([String::static_type()])
                        .build(),
                    // Emitted when an image is successfully loaded into the image area.
                    Signal::builder("image-loaded").build(),
                    // Emitted when an image is successfully saved. The save path is passed as a parameter.
                    Signal::builder("image-saved")
                        .param_types([String::static_type()])
                        .build(),
                    // Emitted when the clear button is clicked.
                    Signal::builder("cleared").build(),
                    // Emitted when the view button is clicked, with the file to be viewed as parameter. If the handler
                    // returns false, the default behavior of launching the file with the OpenURI portal will be
                    // suppressed. Handlers have to return either true or false.
                    Signal::builder("view-requested")
                        .param_types([gio::File::static_type()])
                        .return_type::<bool>()
                        .build(),
                ]
            })
        }
    }

    impl WidgetImpl for ImageArea {}
    impl BinImpl for ImageArea {}
}

// MARK: Wrapper
glib::wrapper! {
    pub struct ImageArea(ObjectSubclass<imp::ImageArea>)
        @extends adw::Bin, gtk::Widget,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

// MARK: Widget
impl ImageArea {
    pub fn new(title: &str) -> Self {
        glib::Object::builder().property("title", title).build()
    }

    pub fn clear(&self) {
        self.imp().clear();
    }
}
