/*
 * convertion.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConfigFormat {
    Json = 0,
    Yaml = 1,
    Toml = 2,
}

impl ConfigFormat {
    fn from_index(index: u32) -> Option<Self> {
        match index {
            0 => Some(ConfigFormat::Json),
            1 => Some(ConfigFormat::Yaml),
            2 => Some(ConfigFormat::Toml),
            _ => None,
        }
    }
}

impl TryFrom<u32> for ConfigFormat {
    type Error = ();

    fn try_from(value: u32) -> Result<Self, Self::Error> {
        ConfigFormat::from_index(value).ok_or(())
    }
}

impl ConfigFormat {
    pub fn to_str(&self) -> &'static str {
        match self {
            ConfigFormat::Json => "json",
            ConfigFormat::Yaml => "yaml",
            ConfigFormat::Toml => "toml",
        }
    }
}

pub fn validate_json(input: &str) -> Result<serde_json::Value, serde_json::Error> {
    serde_json::from_str(input)
}

pub fn validate_yaml(input: &str) -> Result<serde_yaml_ng::Value, String> {
    // Parse as YAML
    let value = serde_yaml_ng::from_str(input).map_err(|e| e.to_string())?;

    // Double-check that it's not JSON
    if let Ok(json_str) = serde_json::to_string(&value) {
        if let Ok(_json_value) = serde_json::from_str::<serde_json::Value>(&json_str) {
            // Check if original input is valid JSON
            if serde_json::from_str::<serde_json::Value>(input.trim()).is_ok() {
                return Err("Input is JSON".to_string());
            }
        }
    }

    Ok(value)
}

pub fn validate_toml(input: &str) -> Result<toml::Value, toml::de::Error> {
    toml::from_str(input)
}

pub fn json_to_yaml(input: &str) -> Result<String, String> {
    let json_value: serde_json::Value = serde_json::from_str(input).unwrap();
    let yaml_string = serde_yaml_ng::to_string(&json_value).map_err(|e| e.to_string())?;
    Ok(yaml_string)
}

pub fn yaml_to_json(input: &str) -> Result<String, String> {
    let yaml_value: serde_yaml_ng::Value = serde_yaml_ng::from_str(input).unwrap();
    let json_string = serde_json::to_string_pretty(&yaml_value).map_err(|e| e.to_string())?;
    Ok(json_string)
}

pub fn toml_to_json(input: &str) -> Result<String, String> {
    let toml_value: toml::Value = toml::from_str(input).unwrap();
    let json_string = serde_json::to_string_pretty(&toml_value).map_err(|e| e.to_string())?;
    Ok(json_string)
}

pub fn json_to_toml(input: &str) -> Result<String, String> {
    let json_value: serde_json::Value = serde_json::from_str(input).unwrap();
    let toml_string = toml::to_string(&json_value).map_err(|e| e.to_string())?;
    Ok(toml_string)
}

pub fn yaml_to_toml(input: &str) -> Result<String, String> {
    let yaml_value: serde_yaml_ng::Value = serde_yaml_ng::from_str(input).unwrap();
    let toml_string = toml::to_string(&yaml_value).map_err(|e| e.to_string())?;
    Ok(toml_string)
}

pub fn toml_to_yaml(input: &str) -> Result<String, String> {
    let toml_value: toml::Value = toml::from_str(input).unwrap();
    let yaml_string = serde_yaml_ng::to_string(&toml_value).map_err(|e| e.to_string())?;
    Ok(yaml_string)
}
