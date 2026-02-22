/*
 * lorem.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use lipsum::lipsum_words_with_rng;
use rand::Rng;

/// Generates a random sentence with the specified number of words.
/// If `length` is `None`, a random length between 5 and 16 words will be used.
///
/// Note: the library adds random punctuation so it may seem that multiple
/// sentences are generated.
pub fn generate_sentence(length: Option<usize>) -> String {
    let length = length.unwrap_or_else(|| rand::thread_rng().gen_range(5..=16));
    lipsum_words_with_rng(rand::thread_rng(), length)
}

/// Generates a random paragraph with the specified number of sentences.
/// If `length` is `None`, a random length between 3 and 7 sentences will be used.
///
/// Note: the library adds random punctuation so it may seem that multiple
/// sentences are generated.
pub fn generate_paragraph(length: Option<usize>) -> String {
    let length = length.unwrap_or_else(|| rand::thread_rng().gen_range(3..=7));
    (0..length)
        .map(|_| generate_sentence(None))
        .collect::<Vec<_>>()
        .join(" ")
}

/// Generates a random text with the specified number of paragraphs.
/// If `length` is `None`, a random length between 3 and 7 paragraphs will be used.
pub fn generate_paragraphs(length: Option<usize>) -> String {
    let length = length.unwrap_or_else(|| rand::thread_rng().gen_range(3..=7));
    (0..length)
        .map(|_| generate_paragraph(None))
        .collect::<Vec<_>>()
        .join("\n\n")
}
