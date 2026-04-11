/*
 * diff.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use similar::{ChangeTag, TextDiff};

#[derive(Debug, Clone, Copy)]
pub enum HighlightType {
    RemovedLine,
    AddedLine,
    Removed,
    Added,
}

pub fn compute_diff(
    old_text: &str,
    new_text: &str,
) -> Result<(String, Vec<(HighlightType, usize, usize)>), String> {
    let diff = TextDiff::from_lines(old_text, new_text);
    let mut output = String::new();
    let mut highlights: Vec<(HighlightType, usize, usize)> = Vec::new();
    let mut line_meta: Vec<(usize, String, ChangeTag)> = Vec::new();

    for change in diff.iter_all_changes() {
        let line_text = change.value().to_string();
        let start_pos = output.len();
        output.push_str(&line_text);

        match change.tag() {
            ChangeTag::Delete => {
                highlights.push((HighlightType::RemovedLine, start_pos, output.len()))
            }
            ChangeTag::Insert => {
                highlights.push((HighlightType::AddedLine, start_pos, output.len()))
            }
            ChangeTag::Equal => {}
        }

        line_meta.push((start_pos, line_text, change.tag()));
    }

    if output.ends_with('\n') {
        output.pop();
    }

    let mut i = 0usize;
    while i < line_meta.len() {
        if line_meta[i].2 == ChangeTag::Delete {
            let del_start = i;
            while i < line_meta.len() && line_meta[i].2 == ChangeTag::Delete {
                i += 1;
            }
            let del_end = i;

            let ins_start = i;
            while i < line_meta.len() && line_meta[i].2 == ChangeTag::Insert {
                i += 1;
            }
            let ins_end = i;

            let pair_count = (del_end - del_start).min(ins_end - ins_start);
            for p in 0..pair_count {
                let (del_line_start, del_line_text, _) = &line_meta[del_start + p];
                let (ins_line_start, ins_line_text, _) = &line_meta[ins_start + p];
                add_char_level_diff_highlights(
                    del_line_text,
                    ins_line_text,
                    *del_line_start,
                    *ins_line_start,
                    &mut highlights,
                );
            }
        } else {
            i += 1;
        }
    }

    Ok((output, highlights))
}

fn add_char_level_diff_highlights(
    removed_line: &str,
    added_line: &str,
    removed_start: usize,
    added_start: usize,
    highlights: &mut Vec<(HighlightType, usize, usize)>,
) {
    let inline = TextDiff::from_chars(removed_line, added_line);
    let mut removed_offset = 0usize;
    let mut added_offset = 0usize;

    for change in inline.iter_all_changes() {
        let len = change.value().len();
        match change.tag() {
            ChangeTag::Delete => {
                if len > 0 {
                    highlights.push((
                        HighlightType::Removed,
                        removed_start + removed_offset,
                        removed_start + removed_offset + len,
                    ));
                }
                removed_offset += len;
            }
            ChangeTag::Insert => {
                if len > 0 {
                    highlights.push((
                        HighlightType::Added,
                        added_start + added_offset,
                        added_start + added_offset + len,
                    ));
                }
                added_offset += len;
            }
            ChangeTag::Equal => {
                removed_offset += len;
                added_offset += len;
            }
        }
    }
}
