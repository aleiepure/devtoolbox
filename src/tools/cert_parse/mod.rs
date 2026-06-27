/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod cert_parse;
mod parser;
pub use cert_parse::CertParseWidget;
use gettextrs::pgettext;

define_tool!(
    widget: CertParseWidget,
    id: "cert_parse",
    title: pgettext("Tool Title", "Certificate Parser"),
    description: pgettext("Tool Description", "Parse and display information from X.509 certificates"),
    sidebar_title: None,
    category: &ToolCategory::Certificates,
    keywords: [
        "x509".to_string(),
        "pem".to_string(),
        "crt".to_string(),
        "ssl".to_string(),
        "tls".to_string(),
        pgettext("Keyword", "security"),
        pgettext("Keyword", "public key"),
        pgettext("Keyword", "private key"),
        pgettext("Keyword", "cryptography"),
    ],
);
