/*
 * timestamp.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{gdk, glib, glib::Properties, CompositeTemplate};

use std::cell::{OnceCell, RefCell};

use adw::prelude::PreferencesGroupExt;
use chrono_tz::TZ_VARIANTS;
use gettextrs::gettext;

mod imp {
    use adw::prelude::ComboRowExt;
    use chrono::{DateTime, Datelike, Local, TimeZone, Timelike};

    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/timestamp/timestamp.ui")]
    #[properties(wrapper_type = super::TimestampWidget)]
    pub struct TimestampWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        tool_options_preferences_group: TemplateChild<adw::PreferencesGroup>,

        #[template_child]
        timestamp_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        day_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        month_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        year_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        hour_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        minute_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        second_spinrow: TemplateChild<adw::SpinRow>,

        #[template_child]
        iso_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        rfc_2822_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        short_date_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        short_time_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        long_date_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        long_time_entryrow: TemplateChild<adw::EntryRow>,

        #[template_child]
        full_long_entryrow: TemplateChild<adw::EntryRow>,

        // Properties
        #[property(set, get, type = String)]
        tool_id: RefCell<String>,

        #[property(set, get, type = String)]
        title: RefCell<String>,

        #[property(set, get, type = String)]
        description: RefCell<String>,

        // Other fields
        /// The timezone ComboRow built programmatically
        timezone_comborow: OnceCell<adw::ComboRow>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for TimestampWidget {
        const NAME: &'static str = "TimestampWidget";
        type Type = super::TimestampWidget;
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
    impl TimestampWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_clicked_timestamp_now_button(&self) {
            let selected_index = self.timezone_comborow.get().unwrap().selected();

            if let Some(tz) = TZ_VARIANTS.get(selected_index as usize) {
                let now = Local::now().with_timezone(tz);
                self.timestamp_spinrow.set_value(now.timestamp() as f64);
            }
        }

        #[template_callback]
        fn on_signal_clicked_timestamp_copy_button(&self) {
            let timestamp = self.timestamp_spinrow.value().to_string();
            let clipboard = gdk::Display::default().unwrap().clipboard();
            clipboard.set_text(&timestamp);
        }

        #[template_callback]
        async fn on_signal_clicked_timestamp_paste_button(&self) {
            let clipboard = gdk::Display::default().unwrap().clipboard();
            let result = clipboard.read_text_future().await;
            match result {
                Ok(Some(text)) => {
                    if let Ok(value) = text.as_str().parse::<f64>() {
                        self.timestamp_spinrow.set_value(value);
                    }
                }
                _ => {}
            }
        }

        #[template_callback]
        fn on_signal_notify_value_timestamp_spinrow(&self) {
            let selected_index = self.timezone_comborow.get().unwrap().selected();

            if let Some(tz) = TZ_VARIANTS.get(selected_index as usize) {
                let timestamp = self.timestamp_spinrow.value() as i64;
                let dt = DateTime::from_timestamp(timestamp, 0)
                    .unwrap()
                    .with_timezone(tz);

                self.day_spinrow.set_value(dt.day() as f64);
                self.month_spinrow.set_value(dt.month() as f64);
                self.year_spinrow.set_value(dt.year() as f64);
                self.hour_spinrow.set_value(dt.hour() as f64);
                self.minute_spinrow.set_value(dt.minute() as f64);
                self.second_spinrow.set_value(dt.second() as f64);
                self.iso_entryrow.set_text(&dt.to_rfc3339());
                self.rfc_2822_entryrow.set_text(&dt.to_rfc2822());
                self.short_date_entryrow
                    .set_text(&dt.format("%Y-%m-%d").to_string());
                self.short_time_entryrow
                    .set_text(&dt.format("%H:%M").to_string());
                self.long_date_entryrow
                    .set_text(&dt.format("%B %d, %Y").to_string());
                self.long_time_entryrow
                    .set_text(&dt.format("%H:%M:%S").to_string());
                self.full_long_entryrow
                    .set_text(&dt.format("%A, %B %d, %Y %H:%M:%S %Z").to_string());
            }
        }

        #[template_callback]
        fn on_signal_clicked_date_now_button(&self) {
            let selected_index = self.timezone_comborow.get().unwrap().selected();

            if let Some(tz) = TZ_VARIANTS.get(selected_index as usize) {
                let now = Local::now().with_timezone(tz);
                self.day_spinrow.set_value(now.day() as f64);
                self.month_spinrow.set_value(now.month() as f64);
                self.year_spinrow.set_value(now.year() as f64);
                self.hour_spinrow.set_value(now.hour() as f64);
                self.minute_spinrow.set_value(now.minute() as f64);
                self.second_spinrow.set_value(now.second() as f64);
            }
        }

        #[template_callback]
        fn on_signal_notify_value_date_spinrow(&self) {
            let selected_index = self.timezone_comborow.get().unwrap().selected();

            if let Some(tz) = TZ_VARIANTS.get(selected_index as usize) {
                let year = self.year_spinrow.value() as i32;
                let month = self.month_spinrow.value() as u32;
                let day = self.day_spinrow.value() as u32;
                let hour = self.hour_spinrow.value() as u32;
                let minute = self.minute_spinrow.value() as u32;
                let second = self.second_spinrow.value() as u32;

                match tz.with_ymd_and_hms(year, month, day, hour, minute, second) {
                    chrono::LocalResult::Single(dt) => {
                        let timestamp = dt.timestamp();
                        self.timestamp_spinrow.set_value(timestamp as f64);
                    }
                    chrono::LocalResult::Ambiguous(dt1, _dt2) => {
                        // During DST transitions, use the first valid result
                        let timestamp = dt1.timestamp();
                        self.timestamp_spinrow.set_value(timestamp as f64);
                    }
                    chrono::LocalResult::None => {
                        // Invalid date/time (e.g., Feb 30, or during DST gap)
                        // let toast = adw::Toast::builder()
                        //     .title(&gettext("Invalid date/time"))
                        //     .build();
                        // self.toast_overlay.add_toast(toast);
                    }
                }
            }
        }

        // Other methods
        /// Build the timezone ComboRow. This is done programmatically to
        /// populate the list with all available timezones from chrono-tz.
        fn build_timezone_comborow(&self) -> adw::ComboRow {
            let list_items = TZ_VARIANTS
                .iter()
                .map(|tz| format!("<item>{}</item>", tz.name()))
                .collect::<Vec<_>>()
                .join("");

            let title = gettext("Timezone");
            let subtitle = gettext("Select the timezone for conversion");

            let combo_row_ui = format!(
                r#"
                <interface>
                    <object class="AdwComboRow" id="timezone_combo_row">
                        <property name="title">{}</property>
                        <property name="subtitle">{}</property>
                        <property name="icon-name">globe</property>
                        <property name="enable-search">true</property>
                        <property name="model">
                            <object class="GtkStringList">
                                <items>
                                    {}
                                </items>
                            </object>
                        </property>
                        <property name="expression">
                            <lookup type="GtkStringObject" name="string"/>
                        </property>
                    </object>
                </interface>
                "#,
                title, subtitle, list_items
            );

            let builder = gtk::Builder::from_string(&combo_row_ui);
            builder.object("timezone_combo_row").unwrap()
        }

        /// Read the system timezone
        fn get_system_timezone(&self) -> Option<String> {
            // from /etc/timezone
            if let Ok(tz) = std::fs::read_to_string("/etc/timezone") {
                return Some(tz.trim().to_string());
            }

            // from /etc/localtime symlink
            if let Ok(localtime_path) = std::fs::read_link("/etc/localtime") {
                if let Some(tz_path) = localtime_path.to_str() {
                    if let Some(pos) = tz_path.find("zoneinfo/") {
                        return Some(tz_path[pos + 9..].to_string());
                    }
                }
            }

            None
        }

        /// Given a timezone name, find its index in the TZ_VARIANTS list.
        fn find_timezone_index(&self, tz_name: &str) -> usize {
            TZ_VARIANTS
                .iter()
                .position(|tz| tz.name() == tz_name)
                .unwrap_or(0)
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for TimestampWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Populate the timezone ComboRow
            let timezone_row = self.build_timezone_comborow();
            self.timezone_comborow.set(timezone_row).unwrap();
            self.tool_options_preferences_group
                .add(self.timezone_comborow.get().unwrap());

            // Set current timezone
            if let Some(tz_name) = self.get_system_timezone() {
                let index = self.find_timezone_index(&tz_name);
                self.timezone_comborow
                    .get()
                    .unwrap()
                    .set_selected(index as u32);
            }

            // Set current date/time
            let now = Local::now();
            self.timestamp_spinrow.set_value(now.timestamp() as f64);
            self.day_spinrow.set_value(now.day() as f64);
            self.month_spinrow.set_value(now.month() as f64);
            self.year_spinrow.set_value(now.year() as f64);
            self.hour_spinrow.set_value(now.hour() as f64);
            self.minute_spinrow.set_value(now.minute() as f64);
            self.second_spinrow.set_value(now.second() as f64);

            self.iso_entryrow.set_text(&now.to_rfc3339());
            self.rfc_2822_entryrow.set_text(&now.to_rfc2822());
            self.short_date_entryrow
                .set_text(&now.format("%Y-%m-%d").to_string());
            self.short_time_entryrow
                .set_text(&now.format("%H:%M").to_string());
            self.long_date_entryrow
                .set_text(&now.format("%B %d, %Y").to_string());
            self.long_time_entryrow
                .set_text(&now.format("%H:%M:%S").to_string());
            self.full_long_entryrow
                .set_text(&now.format("%A, %B %d, %Y %H:%M:%S %Z").to_string());

            // Connect notify handler for timestamp_spinrow
            let obj = self.obj().clone();
            self.timezone_comborow
                .get()
                .unwrap()
                .connect_selected_notify(move |_| {
                    obj.imp().on_signal_notify_value_timestamp_spinrow();
                    obj.imp().on_signal_notify_value_date_spinrow();
                });
        }
    }

    impl WidgetImpl for TimestampWidget {}
    impl BinImpl for TimestampWidget {}
}

glib::wrapper! {
    pub struct TimestampWidget(ObjectSubclass<imp::TimestampWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl TimestampWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
