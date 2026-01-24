/*
 * cron_gen.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use adw::subclass::prelude::*;
use gtk::prelude::*;
use gtk::{glib, glib::Properties, CompositeTemplate};

use adw::prelude::ComboRowExt;
use gettextrs::gettext;

use crate::{
    core::widgets::ActionableEntryRow,
    tools::cron_gen::cron::{CronField, CronMode, CronModeParams},
};

use std::cell::RefCell;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate, Properties)]
    #[template(resource = "/me/iepure/Devtoolbox/tools/cron_gen/cron_gen.ui")]
    #[properties(wrapper_type = super::CronGenWidget)]
    pub struct CronGenWidget {
        // Template widgets
        #[template_child]
        toast_overlay: TemplateChild<adw::ToastOverlay>,

        #[template_child]
        minutes_mode_combo: TemplateChild<adw::ComboRow>,
        #[template_child]
        minutes_interval_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        minutes_starting_at_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        minutes_list_menubutton: TemplateChild<gtk::MenuButton>,
        #[template_child]
        minutes_range_start_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        minutes_range_end_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        minutes_list_grid: TemplateChild<gtk::Grid>,

        #[template_child]
        hours_mode_combo: TemplateChild<adw::ComboRow>,
        #[template_child]
        hours_interval_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        hours_starting_at_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        hours_list_menubutton: TemplateChild<gtk::MenuButton>,
        #[template_child]
        hours_range_start_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        hours_range_end_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        hours_list_grid: TemplateChild<gtk::Grid>,

        #[template_child]
        day_mode_combo: TemplateChild<adw::ComboRow>,
        #[template_child]
        day_interval_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        day_starting_at_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        day_list_menubutton: TemplateChild<gtk::MenuButton>,
        #[template_child]
        day_range_start_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        day_range_end_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        day_list_grid: TemplateChild<gtk::Grid>,

        #[template_child]
        month_mode_combo: TemplateChild<adw::ComboRow>,
        #[template_child]
        month_interval_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        month_starting_at_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        month_list_menubutton: TemplateChild<gtk::MenuButton>,
        #[template_child]
        month_range_start_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        month_range_end_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        month_list_grid: TemplateChild<gtk::Grid>,

        #[template_child]
        dayofweek_mode_combo: TemplateChild<adw::ComboRow>,
        #[template_child]
        dayofweek_interval_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        dayofweek_starting_at_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        dayofweek_list_menubutton: TemplateChild<gtk::MenuButton>,
        #[template_child]
        dayofweek_range_start_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        dayofweek_range_end_spinrow: TemplateChild<adw::SpinRow>,
        #[template_child]
        dayofweek_list_grid: TemplateChild<gtk::Grid>,

        #[template_child]
        command_entryrow: TemplateChild<ActionableEntryRow>,
        #[template_child]
        expression_entryrow: TemplateChild<ActionableEntryRow>,

        // Properties
        #[property(get, set, type = bool, default = false)]
        minutes_every_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        minutes_list_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        minutes_range_visible: RefCell<bool>,

        #[property(get, set, type = bool, default = false)]
        hours_every_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        hours_list_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        hours_range_visible: RefCell<bool>,

        #[property(get, set, type = bool, default = false)]
        day_every_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        day_list_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        day_range_visible: RefCell<bool>,

        #[property(get, set, type = bool, default = false)]
        month_every_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        month_list_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        month_range_visible: RefCell<bool>,

        #[property(get, set, type = bool, default = false)]
        dayofweek_every_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        dayofweek_list_visible: RefCell<bool>,
        #[property(get, set, type = bool, default = false)]
        dayofweek_range_visible: RefCell<bool>,

        // Other fields
        minutes_mode: RefCell<CronMode>,
        minutes_params: RefCell<CronModeParams>,

        hours_mode: RefCell<CronMode>,
        hours_params: RefCell<CronModeParams>,

        day_mode: RefCell<CronMode>,
        day_params: RefCell<CronModeParams>,

        month_mode: RefCell<CronMode>,
        month_params: RefCell<CronModeParams>,

        dayofweek_mode: RefCell<CronMode>,
        dayofweek_params: RefCell<CronModeParams>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for CronGenWidget {
        const NAME: &'static str = "CronGenWidget";
        type Type = super::CronGenWidget;
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
    impl CronGenWidget {
        // Template callbacks and closures
        #[template_callback]
        fn on_signal_notify_selected_minutes_mode(&self) {
            self.handle_mode_change(CronField::Minutes, &self.minutes_mode_combo);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_selected_hours_mode(&self) {
            self.handle_mode_change(CronField::Hours, &self.hours_mode_combo);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_selected_day_mode(&self) {
            self.handle_mode_change(CronField::DayOfMonth, &self.day_mode_combo);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_selected_month_mode(&self) {
            self.handle_mode_change(CronField::Month, &self.month_mode_combo);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_selected_dayofweek_mode(&self) {
            self.handle_mode_change(CronField::DayOfWeek, &self.dayofweek_mode_combo);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_minutes_interval(&self) {
            self.minutes_params.borrow_mut().repeated_interval =
                Some(self.minutes_interval_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_minutes_starting_at(&self) {
            self.minutes_params.borrow_mut().repeated_start =
                Some(self.minutes_starting_at_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_minutes_range_start(&self) {
            self.minutes_params.borrow_mut().range_start =
                Some(self.minutes_range_start_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_minutes_range_end(&self) {
            self.minutes_params.borrow_mut().range_end =
                Some(self.minutes_range_end_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_hours_interval(&self) {
            self.hours_params.borrow_mut().repeated_interval =
                Some(self.hours_interval_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_hours_starting_at(&self) {
            self.hours_params.borrow_mut().repeated_start =
                Some(self.hours_starting_at_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_hours_range_start(&self) {
            self.hours_params.borrow_mut().range_start =
                Some(self.hours_range_start_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_hours_range_end(&self) {
            self.hours_params.borrow_mut().range_end =
                Some(self.hours_range_end_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_day_interval(&self) {
            self.day_params.borrow_mut().repeated_interval =
                Some(self.day_interval_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_day_starting_at(&self) {
            self.day_params.borrow_mut().repeated_start =
                Some(self.day_starting_at_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_day_range_start(&self) {
            self.day_params.borrow_mut().range_start =
                Some(self.day_range_start_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_day_range_end(&self) {
            self.day_params.borrow_mut().range_end =
                Some(self.day_range_end_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_month_interval(&self) {
            self.month_params.borrow_mut().repeated_interval =
                Some(self.month_interval_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_month_starting_at(&self) {
            self.month_params.borrow_mut().repeated_start =
                Some(self.month_starting_at_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_month_range_start(&self) {
            self.month_params.borrow_mut().range_start =
                Some(self.month_range_start_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_month_range_end(&self) {
            self.month_params.borrow_mut().range_end =
                Some(self.month_range_end_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_dayofweek_interval(&self) {
            self.dayofweek_params.borrow_mut().repeated_interval =
                Some(self.dayofweek_interval_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_dayofweek_starting_at(&self) {
            self.dayofweek_params.borrow_mut().repeated_start =
                Some(self.dayofweek_starting_at_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_notify_value_dayofweek_range_start(&self) {
            self.dayofweek_params.borrow_mut().range_start =
                Some(self.dayofweek_range_start_spinrow.value() as u32);
            self.generate_expression();
        }
        #[template_callback]
        fn on_signal_notify_value_dayofweek_range_end(&self) {
            self.dayofweek_params.borrow_mut().range_end =
                Some(self.dayofweek_range_end_spinrow.value() as u32);
            self.generate_expression();
        }

        #[template_callback]
        fn on_signal_changed_command(&self) {
            self.generate_expression();
        }

        // Other methods
        fn handle_mode_change(&self, field: CronField, combo_row: &adw::ComboRow) {
            let selected = combo_row.selected();

            if let Some(mode) = CronMode::from_index(selected) {
                let (params, interval_spin, starting_at_spin, range_start_spin, range_end_spin) =
                    match field {
                        CronField::Minutes => (
                            &self.minutes_params,
                            &self.minutes_interval_spinrow,
                            &self.minutes_starting_at_spinrow,
                            &self.minutes_range_start_spinrow,
                            &self.minutes_range_end_spinrow,
                        ),
                        CronField::Hours => (
                            &self.hours_params,
                            &self.hours_interval_spinrow,
                            &self.hours_starting_at_spinrow,
                            &self.hours_range_start_spinrow,
                            &self.hours_range_end_spinrow,
                        ),
                        CronField::DayOfMonth => (
                            &self.day_params,
                            &self.day_interval_spinrow,
                            &self.day_starting_at_spinrow,
                            &self.day_range_start_spinrow,
                            &self.day_range_end_spinrow,
                        ),
                        CronField::Month => (
                            &self.month_params,
                            &self.month_interval_spinrow,
                            &self.month_starting_at_spinrow,
                            &self.month_range_start_spinrow,
                            &self.month_range_end_spinrow,
                        ),
                        CronField::DayOfWeek => (
                            &self.dayofweek_params,
                            &self.dayofweek_interval_spinrow,
                            &self.dayofweek_starting_at_spinrow,
                            &self.dayofweek_range_start_spinrow,
                            &self.dayofweek_range_end_spinrow,
                        ),
                    };

                // Copy current params to avoid holding a borrow while setting spin values
                let (repeated_interval, repeated_start, range_start, range_end) = {
                    let p = params.borrow();
                    (
                        p.repeated_interval,
                        p.repeated_start,
                        p.range_start,
                        p.range_end,
                    )
                };

                match mode {
                    CronMode::Repeated => {
                        if let Some(interval) = repeated_interval {
                            interval_spin.set_value(interval as f64);
                        }
                        if let Some(start) = repeated_start {
                            starting_at_spin.set_value(start as f64);
                        }
                    }
                    CronMode::Range => {
                        if let Some(start) = range_start {
                            range_start_spin.set_value(start as f64);
                        }
                        if let Some(end) = range_end {
                            range_end_spin.set_value(end as f64);
                        }
                    }
                    _ => {}
                }

                // Store the new mode
                match field {
                    CronField::Minutes => *self.minutes_mode.borrow_mut() = mode,
                    CronField::Hours => *self.hours_mode.borrow_mut() = mode,
                    CronField::DayOfMonth => *self.day_mode.borrow_mut() = mode,
                    CronField::Month => *self.month_mode.borrow_mut() = mode,
                    CronField::DayOfWeek => *self.dayofweek_mode.borrow_mut() = mode,
                }

                self.update_field_visibility(field, mode);
                self.generate_expression();
            }
        }

        fn update_field_visibility(&self, field: CronField, mode: CronMode) {
            let obj = self.obj();

            let (set_every, set_list, set_range): (
                Box<dyn Fn(bool)>,
                Box<dyn Fn(bool)>,
                Box<dyn Fn(bool)>,
            ) = match field {
                CronField::Minutes => (
                    Box::new(|v| obj.set_minutes_every_visible(v)),
                    Box::new(|v| obj.set_minutes_list_visible(v)),
                    Box::new(|v| obj.set_minutes_range_visible(v)),
                ),
                CronField::Hours => (
                    Box::new(|v| obj.set_hours_every_visible(v)),
                    Box::new(|v| obj.set_hours_list_visible(v)),
                    Box::new(|v| obj.set_hours_range_visible(v)),
                ),
                CronField::DayOfMonth => (
                    Box::new(|v| obj.set_day_every_visible(v)),
                    Box::new(|v| obj.set_day_list_visible(v)),
                    Box::new(|v| obj.set_day_range_visible(v)),
                ),
                CronField::Month => (
                    Box::new(|v| obj.set_month_every_visible(v)),
                    Box::new(|v| obj.set_month_list_visible(v)),
                    Box::new(|v| obj.set_month_range_visible(v)),
                ),
                CronField::DayOfWeek => (
                    Box::new(|v| obj.set_dayofweek_every_visible(v)),
                    Box::new(|v| obj.set_dayofweek_list_visible(v)),
                    Box::new(|v| obj.set_dayofweek_range_visible(v)),
                ),
            };

            match mode {
                CronMode::Every => {
                    set_every(false);
                    set_list(false);
                    set_range(false);
                }
                CronMode::Repeated => {
                    set_every(true);
                    set_list(false);
                    set_range(false);
                }
                CronMode::List => {
                    set_every(false);
                    set_list(true);
                    set_range(false);
                }
                CronMode::Range => {
                    set_every(false);
                    set_list(false);
                    set_range(true);
                }
            }
        }

        fn populate_list_popover(
            &self,
            field: CronField,
            grid: &gtk::Grid,
            _params: &RefCell<CronModeParams>,
            _menubutton: &gtk::MenuButton,
        ) {
            let range = field.range();
            let cols = field.grid_columns();

            for value in 0..range {
                let label = Self::value_label(field, value);

                let check_button = gtk::CheckButton::with_label(&label);
                check_button.set_tooltip_text(Some(&field.label_select()));

                let weak_self = self.downgrade();
                check_button.connect_toggled(move |_| {
                    if let Some(widget) = weak_self.upgrade() {
                        widget.update_list_selection(field, value);
                        widget.generate_expression();
                    }
                });

                grid.attach(
                    &check_button,
                    (value % cols) as i32,
                    (value / cols) as i32,
                    1,
                    1,
                );
            }
        }

        fn update_list_selection(&self, field: CronField, value: u32) {
            let (params, menubutton) = match field {
                CronField::Minutes => (&self.minutes_params, &self.minutes_list_menubutton),
                CronField::Hours => (&self.hours_params, &self.hours_list_menubutton),
                CronField::DayOfMonth => (&self.day_params, &self.day_list_menubutton),
                CronField::Month => (&self.month_params, &self.month_list_menubutton),
                CronField::DayOfWeek => (&self.dayofweek_params, &self.dayofweek_list_menubutton),
            };

            let mut p = params.borrow_mut();
            let values = p.values.get_or_insert_with(Vec::new);

            if values.contains(&value) {
                values.retain(|&x| x != value);
            } else {
                values.push(value);
            }

            if values.is_empty() {
                menubutton.set_label(&field.label_any());
            } else {
                values.sort();
                let labels: Vec<String> = values
                    .iter()
                    .map(|v| Self::value_label(field, *v))
                    .collect();
                let labels_joined = labels.join(", ");

                if labels_joined.len() > 20 {
                    menubutton.set_label(&gettext("Multiple selected"));
                } else {
                    menubutton.set_label(&labels_joined);
                }
            }
        }

        fn value_label(field: CronField, value: u32) -> String {
            match field {
                CronField::Minutes | CronField::Hours => value.to_string(),
                CronField::DayOfMonth => (value + 1).to_string(),
                CronField::Month => {
                    let months = [
                        gettext("January"),
                        gettext("February"),
                        gettext("March"),
                        gettext("April"),
                        gettext("May"),
                        gettext("June"),
                        gettext("July"),
                        gettext("August"),
                        gettext("September"),
                        gettext("October"),
                        gettext("November"),
                        gettext("December"),
                    ];
                    months[value as usize].chars().take(3).collect()
                }
                CronField::DayOfWeek => {
                    let days = [
                        gettext("Sunday"),
                        gettext("Monday"),
                        gettext("Tuesday"),
                        gettext("Wednesday"),
                        gettext("Thursday"),
                        gettext("Friday"),
                        gettext("Saturday"),
                    ];
                    days[value as usize].chars().take(3).collect()
                }
            }
        }

        fn populate_minutes_list_popover(&self) {
            self.populate_list_popover(
                CronField::Minutes,
                &self.minutes_list_grid,
                &self.minutes_params,
                &self.minutes_list_menubutton,
            );
        }

        fn populate_hours_list_popover(&self) {
            self.populate_list_popover(
                CronField::Hours,
                &self.hours_list_grid,
                &self.hours_params,
                &self.hours_list_menubutton,
            );
        }

        fn populate_day_list_popover(&self) {
            self.populate_list_popover(
                CronField::DayOfMonth,
                &self.day_list_grid,
                &self.day_params,
                &self.day_list_menubutton,
            );
        }

        fn populate_month_list_popover(&self) {
            self.populate_list_popover(
                CronField::Month,
                &self.month_list_grid,
                &self.month_params,
                &self.month_list_menubutton,
            );
        }

        fn populate_dayofweek_list_popover(&self) {
            self.populate_list_popover(
                CronField::DayOfWeek,
                &self.dayofweek_list_grid,
                &self.dayofweek_params,
                &self.dayofweek_list_menubutton,
            );
        }

        fn generate_expression(&self) {
            let minutes_part = self
                .minutes_mode
                .borrow()
                .to_cron_string(&self.minutes_params.borrow());
            let hours_part = self
                .hours_mode
                .borrow()
                .to_cron_string(&self.hours_params.borrow());
            let day_part = self
                .day_mode
                .borrow()
                .to_cron_string(&self.day_params.borrow());
            let month_part = self
                .month_mode
                .borrow()
                .to_cron_string(&self.month_params.borrow());
            let dayofweek_part = self
                .dayofweek_mode
                .borrow()
                .to_cron_string(&self.dayofweek_params.borrow());

            self.expression_entryrow.set_text(&format!(
                "{} {} {} {} {} {}",
                minutes_part,
                hours_part,
                day_part,
                month_part,
                dayofweek_part,
                self.command_entryrow.text()
            ));
        }
    }

    #[glib::derived_properties]
    impl ObjectImpl for CronGenWidget {
        fn constructed(&self) {
            self.parent_constructed();

            // Populate popovers
            self.populate_minutes_list_popover();
            self.populate_hours_list_popover();
            self.populate_day_list_popover();
            self.populate_month_list_popover();
            self.populate_dayofweek_list_popover();

            self.generate_expression();
        }
    }

    impl WidgetImpl for CronGenWidget {}
    impl BinImpl for CronGenWidget {}
}

glib::wrapper! {
    pub struct CronGenWidget(ObjectSubclass<imp::CronGenWidget>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget, gtk::Orientable;
}

impl CronGenWidget {
    pub fn new() -> Self {
        glib::Object::builder().build()
    }
}
