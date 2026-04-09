/*
 * qrcode.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gdk, gio, glib, glib::Properties, CompositeTemplate};

use std::cell::RefCell;

use std::error::Error;

use adw::prelude::ComboRowExt;
use gettextrs::gettext;

use crate::{
    core::widgets::{ActionableEntryRow, ImageArea},
    tools::qrcode::generator::*,
};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/devtoolbox/tools/qrcode/qrcode.ui")]
    #[properties(wrapper_type = super::QrcodeWidget)]
    pub struct QrcodeWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        type_comborow: TemplateChild<adw::ComboRow>,

        // Text/URL fields
        #[template_child]
        text_entryrow: TemplateChild<ActionableEntryRow>,

        // Geo location fields
        #[template_child]
        geo_lat_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        geo_lon_entryrow: TemplateChild<ActionableEntryRow>,

        // WiFi fields
        #[template_child]
        wifi_ssid_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        wifi_security_comborow: TemplateChild<adw::ComboRow>,

        #[template_child]
        wifi_password_entryrow: TemplateChild<adw::PasswordEntryRow>,

        #[template_child]
        wifi_hidden_switchrow: TemplateChild<adw::SwitchRow>,

        // Contact fields
        #[template_child]
        contact_first_name_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_last_name_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_phone_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_email_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_birthdate_menubutton: TemplateChild<gtk::MenuButton>,

        #[template_child]
        contact_birthdate_not_set_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        contact_birthdate_calendar_checkbutton: TemplateChild<gtk::CheckButton>,

        #[template_child]
        contact_birthdate_calendar: TemplateChild<gtk::Calendar>,

        #[template_child]
        contact_url_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_address_street_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_address_city_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_address_state_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_address_postal_code_entryrow: TemplateChild<ActionableEntryRow>,

        #[template_child]
        contact_address_country_entryrow: TemplateChild<ActionableEntryRow>,

        // Image area
        #[template_child]
        imagearea: TemplateChild<ImageArea>,

        // Properties (if not needed, remove Properties derive and this section)
        #[property(set, get, type = bool, default = false)]
        dragging: RefCell<bool>,

        // Other fields
        saved_file: RefCell<Option<gio::File>>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for QrcodeWidget {
        const NAME: &'static str = "QrcodeWidget";
        type Type = super::QrcodeWidget;
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
    impl QrcodeWidget {
        // Closures
        #[template_callback]
        fn is_text_url_closure(&self, type_index: u32) -> bool {
            if QrcodeType::from_index(type_index) == Some(QrcodeType::TextUrl) {
                true
            } else {
                false
            }
        }

        #[template_callback]
        fn is_geo_location_closure(&self, type_index: u32) -> bool {
            if QrcodeType::from_index(type_index) == Some(QrcodeType::GeoLocation) {
                true
            } else {
                false
            }
        }

        #[template_callback]
        fn is_wifi_closure(&self, type_index: u32) -> bool {
            if QrcodeType::from_index(type_index) == Some(QrcodeType::Wifi) {
                true
            } else {
                false
            }
        }

        #[template_callback]
        fn is_wifi_needs_password_closure(&self, type_index: u32, security_index: u32) -> bool {
            if QrcodeType::from_index(type_index) == Some(QrcodeType::Wifi)
                && WifiSecurity::from_index(security_index) != Some(WifiSecurity::None)
            {
                true
            } else {
                false
            }
        }

        #[template_callback]
        fn is_contact_closure(&self, type_index: u32) -> bool {
            if QrcodeType::from_index(type_index) == Some(QrcodeType::Contact) {
                true
            } else {
                false
            }
        }

        // Signal handlers
        #[template_callback]
        fn on_signal_notify_selected_type_comborow(&self) {
            self.do_generation();
        }

        #[template_callback]
        fn on_signal_changed_entryrow(&self) {
            self.do_generation();
        }

        #[template_callback]
        fn on_signal_notify_selected_wifi_security_comborow(&self) {
            self.do_generation();
        }

        #[template_callback]
        fn on_signal_notify_active_wifi_hidden_switchrow(&self) {
            self.do_generation();
        }

        #[template_callback]
        fn on_signal_toggled_contact_birthdate_not_set_checkbutton(&self) {
            if self.contact_birthdate_not_set_checkbutton.is_active() {
                self.contact_birthdate_menubutton
                    .set_label(&gettext("Not Set"));
            } else {
                self.contact_birthdate_menubutton
                    .set_label(&self.contact_birthdate_calendar.date().format("%x").unwrap());
            }

            self.do_generation();
        }

        #[template_callback]
        fn on_signal_day_selected_contact_birthdate_calendar(&self) {
            self.contact_birthdate_calendar_checkbutton.set_active(true);
            self.contact_birthdate_menubutton
                .set_label(&self.contact_birthdate_calendar.date().format("%x").unwrap());
            self.do_generation();
        }

        #[template_callback]
        fn on_signal_error_imagearea(&self, error_message: String) {
            let toast = adw::Toast::builder().title(error_message).build();
            self.toast_overlay.add_toast(toast);
        }

        #[template_callback]
        fn on_signal_image_saved_imagearea(&self, save_path: String) {
            // Store the saved file
            let file = gio::File::for_path(save_path.clone());
            self.saved_file.replace(Some(file.clone()));

            // Show toast with "Open" button
            let obj = self.obj().clone();
            let toast = adw::Toast::builder()
                .title(gettext("Image saved"))
                .button_label("Open")
                .build();
            toast.connect_button_clicked(move |_| {
                let parent = obj.root().and_downcast::<gtk::Window>();
                let file = file.clone();
                glib::spawn_future_local(async move {
                    let launcher = gtk::FileLauncher::new(Some(&file));
                    launcher
                        .launch_future(parent.as_ref())
                        .await
                        .unwrap_or_else(|err| {
                            eprintln!("Failed to launch file: {}", err);
                        });
                });
            });
            self.toast_overlay.add_toast(toast);
        }

        // Other methods
        fn do_generation(&self) {
            match QrcodeType::from_index(self.type_comborow.selected() as u32) {
                Some(QrcodeType::TextUrl) => self.do_text_url_generation(),
                Some(QrcodeType::GeoLocation) => self.do_geo_location_generation(),
                Some(QrcodeType::Wifi) => self.do_wifi_generation(),
                Some(QrcodeType::Contact) => self.do_contact_generation(),
                _ => unreachable!("Invalid QR code type index"),
            }
        }

        fn do_text_url_generation(&self) {
            // Input validation
            if self.text_entryrow.text().is_empty() {
                self.imagearea.clear();
                return;
            }

            let text = self.text_entryrow.text();

            let gen_result: Result<gio::File, Box<dyn Error>> = generate_from_text(&text);
            match gen_result {
                Ok(file) => {
                    self.imagearea.set_file(Some(&file));
                }
                Err(e) => {
                    let toast = adw::Toast::builder().title(format!("{e}")).build();
                    self.toast_overlay.add_toast(toast);
                }
            }
        }

        fn do_geo_location_generation(&self) {
            let lat_text = self.geo_lat_entryrow.text();
            let lon_text = self.geo_lon_entryrow.text();

            if lat_text.is_empty() && lon_text.is_empty() {
                self.imagearea.clear();
                self.geo_lat_entryrow.remove_css_class("error");
                self.geo_lon_entryrow.remove_css_class("error");
                return;
            }

            let mut lat_valid = false;
            let mut lon_valid = false;

            // Validate latitude
            if !lat_text.is_empty() {
                if lat_text.trim_start_matches('+').parse::<f64>().is_ok() {
                    self.geo_lat_entryrow.remove_css_class("error");
                    lat_valid = true;
                } else {
                    self.geo_lat_entryrow.add_css_class("error");
                }
            } else {
                self.geo_lat_entryrow.remove_css_class("error");
            }

            // Validate longitude
            if !lon_text.is_empty() {
                if lon_text.trim_start_matches('+').parse::<f64>().is_ok() {
                    self.geo_lon_entryrow.remove_css_class("error");
                    lon_valid = true;
                } else {
                    self.geo_lon_entryrow.add_css_class("error");
                }
            } else {
                self.geo_lon_entryrow.remove_css_class("error");
            }

            // Only generate if both are valid and non-empty
            if lat_valid && lon_valid {
                let lat = lat_text.trim_start_matches('+');
                let lon = lon_text.trim_start_matches('+');
                let gen_result: Result<gio::File, Box<dyn Error>> = generate_from_lat_lon(lat, lon);
                match gen_result {
                    Ok(file) => {
                        self.imagearea.set_file(Some(&file));
                    }
                    Err(e) => {
                        self.imagearea.set_error(true);
                        self.imagearea.set_error_label(format!("{e}"));
                    }
                }
            } else if !lat_text.is_empty() && !lon_text.is_empty() {
                // Both fields filled, but at least one is invalid
                self.imagearea.set_error(true);
                self.imagearea
                    .set_error_label(gettext("Showing QR code with previous valid data"));
            }
            // If one or both fields are empty, do nothing (do not clear image area or set error)
        }

        fn do_wifi_generation(&self) {
            let ssid = self.wifi_ssid_entryrow.text();
            let security_index = self.wifi_security_comborow.selected() as u32;
            let password = self.wifi_password_entryrow.text();
            let hidden = self.wifi_hidden_switchrow.is_active();

            if ssid.is_empty() {
                self.imagearea.clear();
                return;
            }

            let security = WifiSecurity::from_index(security_index).unwrap_or(WifiSecurity::None);

            if security != WifiSecurity::None && password.is_empty() {
                self.wifi_password_entryrow.add_css_class("error");
                self.imagearea.set_error(true);
                self.imagearea
                    .set_error_label(gettext("Showing QR code with previous valid data"));
                return;
            } else {
                self.wifi_password_entryrow.remove_css_class("error");
            }

            let gen_result: Result<gio::File, Box<dyn Error>> =
                generate_from_wifi(&ssid, security, &password, hidden);
            match gen_result {
                Ok(file) => {
                    self.imagearea.set_file(Some(&file));
                }
                Err(e) => {
                    self.imagearea.set_error(true);
                    self.imagearea.set_error_label(format!("{e}"));
                }
            }
        }

        fn do_contact_generation(&self) {
            let first_name = self.contact_first_name_entryrow.text();
            let last_name = self.contact_last_name_entryrow.text();
            let phone = self.contact_phone_entryrow.text();
            let email = self.contact_email_entryrow.text();
            let url = self.contact_url_entryrow.text();
            let address_street = self.contact_address_street_entryrow.text();
            let address_city = self.contact_address_city_entryrow.text();
            let address_state = self.contact_address_state_entryrow.text();
            let address_postal_code = self.contact_address_postal_code_entryrow.text();
            let address_country = self.contact_address_country_entryrow.text();

            let birthdate_not_set = self.contact_birthdate_not_set_checkbutton.is_active();
            let birthdate_calendar_active = self.contact_birthdate_calendar_checkbutton.is_active();

            let birthdate = if birthdate_not_set {
                None
            } else if birthdate_calendar_active {
                let date = self.contact_birthdate_calendar.date();
                Some((date.year(), date.month() + 1, date.day_of_month()))
            } else {
                None
            };

            if first_name.is_empty() || last_name.is_empty() {
                self.imagearea.clear();
                return;
            }

            let address = if address_street.is_empty()
                && address_city.is_empty()
                && address_state.is_empty()
                && address_postal_code.is_empty()
                && address_country.is_empty()
            {
                None
            } else {
                Some((
                    &address_street.to_string(),
                    &address_city.to_string(),
                    &address_state.to_string(),
                    &address_postal_code.to_string(),
                    &address_country.to_string(),
                ))
            };

            let gen_result: Result<gio::File, Box<dyn Error>> = generate_from_contact(
                &first_name,
                &last_name,
                Some(&phone),
                Some(&email),
                birthdate,
                Some(&url),
                address,
            );

            match gen_result {
                Ok(file) => {
                    self.imagearea.set_file(Some(&file));
                }
                Err(e) => {
                    self.imagearea.set_error(true);
                    self.imagearea.set_error_label(format!("{e}"));
                }
            }
        }
    }

    impl ObjectImpl for QrcodeWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Drag and drop
            let drop_target =
                gtk::DropTarget::new(gdk::FileList::static_type(), gdk::DragAction::COPY);

            let obj = self.obj().clone();
            drop_target.connect_enter(move |_, _, _| {
                obj.set_dragging(true);
                gdk::DragAction::COPY
            });

            let obj = self.obj().clone();
            drop_target.connect_leave(move |_| {
                obj.set_dragging(false);
            });

            self.obj().add_controller(drop_target);
        }
    }

    impl WidgetImpl for QrcodeWidget {}
    impl BinImpl for QrcodeWidget {}
}

glib::wrapper! {
    pub struct QrcodeWidget(ObjectSubclass<imp::QrcodeWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl QrcodeWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
