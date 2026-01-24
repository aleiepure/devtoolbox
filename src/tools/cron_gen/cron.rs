/*
 * cron.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use gettextrs::gettext;

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum CronMode {
    /// Every unit (e.g., every minute)
    #[default]
    Every,
    /// Repeated at intervals (e.g., every 5 minutes)
    Repeated,
    /// Specific values (e.g., at minutes 0, 15, 30, 45)
    List,
    /// Range of values (e.g., from minute 10 to 20)
    Range,
}

impl CronMode {
    /// Convert from index to CronMode
    pub fn from_index(index: u32) -> Option<Self> {
        match index {
            0 => Some(CronMode::Every),
            1 => Some(CronMode::Repeated),
            2 => Some(CronMode::List),
            3 => Some(CronMode::Range),
            _ => None,
        }
    }

    /// Generate CRON string representation
    pub fn to_cron_string(&self, params: &CronModeParams) -> String {
        match self {
            CronMode::Every => "*".to_string(),
            CronMode::Repeated => format!(
                "{}/{}",
                params.repeated_start.unwrap_or(0),
                params.repeated_interval.unwrap_or(1)
            ),
            CronMode::List => match &params.values {
                Some(values) => values
                    .iter()
                    .map(|v| v.to_string())
                    .collect::<Vec<_>>()
                    .join(","),
                None => "*".to_string(),
            },
            CronMode::Range => format!(
                "{}-{}",
                params.range_start.unwrap_or(0),
                params.range_end.unwrap_or(0)
            ),
        }
    }
}

/// Parameters associated with each CronMode
#[derive(Debug, Clone)]
pub struct CronModeParams {
    pub repeated_interval: Option<u32>, // For Repeated mode
    pub repeated_start: Option<u32>,    // For Repeated mode
    pub range_start: Option<u32>,       // For Range mode
    pub range_end: Option<u32>,         // For Range mode
    pub values: Option<Vec<u32>>,       // For List mode
}

impl Default for CronModeParams {
    fn default() -> Self {
        CronModeParams {
            repeated_interval: None,
            repeated_start: None,
            range_start: None,
            range_end: None,
            values: None,
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub enum CronField {
    Minutes,
    Hours,
    DayOfMonth,
    Month,
    DayOfWeek,
}

impl CronField {
    pub fn range(&self) -> u32 {
        match self {
            CronField::Minutes => 60,
            CronField::Hours => 24,
            CronField::DayOfMonth => 31,
            CronField::Month => 12,
            CronField::DayOfWeek => 7,
        }
    }

    pub fn grid_columns(&self) -> u32 {
        match self {
            CronField::Minutes | CronField::Hours | CronField::DayOfMonth => 10,
            CronField::Month => 4,
            CronField::DayOfWeek => 7,
        }
    }

    pub fn label_any(&self) -> String {
        match self {
            CronField::Minutes => gettext("Any minute"),
            CronField::Hours => gettext("Any hour"),
            CronField::DayOfMonth => gettext("Any day"),
            CronField::Month => gettext("Any month"),
            CronField::DayOfWeek => gettext("Any day of week"),
        }
    }

    pub fn label_select(&self) -> String {
        match self {
            CronField::Minutes => gettext("Select minutes"),
            CronField::Hours => gettext("Select hours"),
            CronField::DayOfMonth => gettext("Select days"),
            CronField::Month => gettext("Select months"),
            CronField::DayOfWeek => gettext("Select days of week"),
        }
    }
}
