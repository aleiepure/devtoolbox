/*
 * generator.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use gtk::gio;
use image::Luma;
use qrcode::QrCode;
use sourceview::prelude::FileExt;

// QR code types
#[derive(Debug, PartialEq, Clone, Copy)]
pub enum QrcodeType {
    TextUrl,
    GeoLocation,
    Wifi,
    Contact,
}

pub trait QrcodeTypeImpl {
    fn from_index(index: u32) -> Option<Self>
    where
        Self: Sized;
}

impl QrcodeTypeImpl for QrcodeType {
    fn from_index(index: u32) -> Option<Self> {
        match index {
            0 => Some(QrcodeType::TextUrl),
            1 => Some(QrcodeType::GeoLocation),
            2 => Some(QrcodeType::Wifi),
            3 => Some(QrcodeType::Contact),
            _ => unreachable!("Invalid type index: {index}"),
        }
    }
}

// WiFi security types
#[derive(Debug, PartialEq, Clone, Copy)]
pub enum WifiSecurity {
    None,
    WEP,
    WpaWpa2,
    Wpa3Personal,
}

pub trait WifiSecurityImpl {
    fn from_index(index: u32) -> Option<Self>
    where
        Self: Sized;
}

impl WifiSecurityImpl for WifiSecurity {
    fn from_index(index: u32) -> Option<Self> {
        match index {
            0 => Some(WifiSecurity::None),
            1 => Some(WifiSecurity::WEP),
            2 => Some(WifiSecurity::WpaWpa2),
            3 => Some(WifiSecurity::Wpa3Personal),
            _ => unreachable!("Invalid security type index: {index}"),
        }
    }
}

pub fn generate_from_text(text: &str) -> Result<gio::File, Box<dyn std::error::Error>> {
    // QR code generation
    let code = QrCode::new(text.as_bytes()).map_err(|e| format!("QR error: {e}"))?;
    let image = code.render::<Luma<u8>>().build();

    let file = gio::File::new_tmp(Some(&"devtoolbox_XXXXXX.png"));
    match file {
        Ok(file_and_stream) => {
            let file = file_and_stream.0;
            let path = file.path().ok_or("Failed to get temporary file path")?;
            image
                .save(&path)
                .map_err(|e| format!("Image save error: {e}"))?;
            Ok(file)
        }
        Err(e) => Err(format!("Temporary file error: {e}").into()),
    }
}
pub fn generate_from_lat_lon(
    lat: &str,
    lon: &str,
) -> Result<gio::File, Box<dyn std::error::Error>> {
    generate_from_text(&format!("geo:{lat},{lon}"))
}

pub fn generate_from_wifi(
    ssid: &str,
    security: WifiSecurity,
    password: &str,
    hidden: bool,
) -> Result<gio::File, Box<dyn std::error::Error>> {
    let security_str = match security {
        WifiSecurity::None => "nopass",
        WifiSecurity::WEP => "WEP",
        WifiSecurity::WpaWpa2 => "WPA",
        WifiSecurity::Wpa3Personal => "WPA3",
    };
    let ssid_encoded = mecard_encode(ssid);
    let mut encoded_string = format!("WIFI:T:{security_str};S:{ssid_encoded};");
    if security != WifiSecurity::None {
        let password_encoded = mecard_encode(password);
        encoded_string.push_str(&format!("P:{password_encoded};"));
    }
    if hidden {
        encoded_string.push_str("H:true;");
    }
    encoded_string.push_str(";");
    generate_from_text(&encoded_string)
}

pub fn generate_from_contact(
    first_name: &str,
    last_name: &str,
    phone: Option<&str>,
    email: Option<&str>,
    birthdate: Option<(i32, i32, i32)>, // (year, month, day)
    url: Option<&str>,
    address: Option<(&String, &String, &String, &String, &String)>, // (street, city, state, postal code, country)
) -> Result<gio::File, Box<dyn std::error::Error>> {
    let name = format!("{},{}", last_name, first_name);
    let address = if let Some((street, city, state, postal_code, country)) = address {
        format!("ADR:;;{street};{city};{state};{postal_code};{country}")
    } else {
        String::new()
    };

    let mut encoded_string = String::new();
    encoded_string.push_str("BEGIN:VCARD\n");
    encoded_string.push_str("VERSION:3.0\n");
    encoded_string.push_str(&format!("FN:{name}\n"));
    if let Some(phone) = phone {
        if !phone.is_empty() {
            encoded_string.push_str(&format!("TEL:{phone}\n"));
        }
    }
    if let Some(email) = email {
        if !email.is_empty() {
            encoded_string.push_str(&format!("EMAIL:{email}\n"));
        }
    }
    if let Some((year, month, day)) = birthdate {
        encoded_string.push_str(&format!("BDAY:{year}{month}{day}\n"));
    }
    if let Some(url) = url {
        if !url.is_empty() {
            encoded_string.push_str(&format!("URL:{url}\n"));
        }
    }
    if !address.is_empty() {
        encoded_string.push_str(&format!("ADR:{address}\n"));
    }
    encoded_string.push_str("END:VCARD");

    generate_from_text(&encoded_string)
}

fn mecard_encode(input: &str) -> String {
    input
        .replace('\\', "\\\\")
        .replace(';', "\\;")
        .replace(',', "\\,")
        .replace('\"', "\\\"")
        .replace(':', "\\:")
}
