/*
 * mod.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use crate::define_tool;
use crate::tools::macros::ToolCategory;

mod hash;
use gettextrs::pgettext;
pub use hash::HashWidget;

define_tool!(
    widget: HashWidget,
    id: "hash",
    title: pgettext("Tool Title", "Hash"),
    description: pgettext("Tool Description", "Calculate file hashes and check for integrity"),
    sidebar_title: None,
    category: &ToolCategory::Generators,
    keywords: [
        pgettext("keyword", "checksum"),
        pgettext("keyword", "digest"),
        pgettext("keyword", "security"),
        pgettext("keyword", "cryptography"),
        pgettext("keyword", "md5"),
        pgettext("keyword", "sha1"),
        pgettext("keyword", "sha256"),
        pgettext("keyword", "sha512"),
        pgettext("keyword", "sha3"),
        pgettext("keyword", "blake3"),
    ],
);
