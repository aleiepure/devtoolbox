/*
 * string_cases.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

pub trait StringCase {
    fn to_sentence_case(&self) -> String;
    fn to_title_case(&self) -> String;
    fn to_camel_case(&self) -> String;
    fn to_pascal_case(&self) -> String;
    fn to_snake_case(&self) -> String;
    fn to_constant_case(&self) -> String;
    fn to_kebab_case(&self) -> String;
    fn to_cobol_case(&self) -> String;
    fn to_train_case(&self) -> String;
    fn to_dot_case(&self) -> String;
    fn to_alternating_case(&self) -> String;
    fn to_reverse_alternating_case(&self) -> String;
}

fn map_lines(input: &str, mut transform: impl FnMut(&str) -> String) -> String {
    input
        .split('\n')
        .map(|line| transform(line))
        .collect::<Vec<String>>()
        .join("\n")
}

impl StringCase for String {
    fn to_sentence_case(&self) -> String {
        let mut chars = self.chars();
        match chars.next() {
            None => String::new(),
            Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
        }
    }

    fn to_title_case(&self) -> String {
        map_lines(self, |line| {
            line.split_whitespace()
                .map(|word| {
                    let mut chars = word.chars();
                    match chars.next() {
                        None => String::new(),
                        Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
                    }
                })
                .collect::<Vec<String>>()
                .join(" ")
        })
    }

    fn to_camel_case(&self) -> String {
        map_lines(self, |line| {
            let mut result = String::new();
            let mut capitalize_next = false;

            for c in line.chars() {
                if c.is_whitespace() || c == '_' || c == '-' {
                    capitalize_next = true;
                } else if capitalize_next {
                    result.push_str(&c.to_uppercase().to_string());
                    capitalize_next = false;
                } else {
                    result.push(c);
                }
            }

            result
        })
    }

    fn to_pascal_case(&self) -> String {
        map_lines(self, |line| {
            line.split_whitespace()
                .map(|word| {
                    let mut chars = word.chars();
                    match chars.next() {
                        None => String::new(),
                        Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
                    }
                })
                .collect::<Vec<String>>()
                .join("")
        })
    }

    fn to_snake_case(&self) -> String {
        map_lines(self, |line| {
            line.split_whitespace()
                .map(|word| word.to_lowercase())
                .collect::<Vec<String>>()
                .join("_")
        })
    }

    fn to_constant_case(&self) -> String {
        self.to_snake_case().to_uppercase()
    }

    fn to_kebab_case(&self) -> String {
        map_lines(self, |line| {
            line.split_whitespace()
                .map(|word| word.to_lowercase())
                .collect::<Vec<String>>()
                .join("-")
        })
    }

    fn to_cobol_case(&self) -> String {
        map_lines(self, |line| {
            line.split_whitespace()
                .map(|word| word.to_uppercase())
                .collect::<Vec<String>>()
                .join("-")
        })
    }

    fn to_train_case(&self) -> String {
        map_lines(self, |line| {
            line.split_whitespace()
                .map(|word| {
                    let mut chars = word.chars();
                    match chars.next() {
                        None => String::new(),
                        Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
                    }
                })
                .collect::<Vec<String>>()
                .join("-")
        })
    }

    fn to_dot_case(&self) -> String {
        map_lines(self, |line| {
            line.split_whitespace()
                .map(|word| word.to_lowercase())
                .collect::<Vec<String>>()
                .join(".")
        })
    }

    fn to_alternating_case(&self) -> String {
        let mut result = String::new();
        let mut uppercase = true;

        for c in self.chars() {
            if c.is_whitespace() {
                result.push(c);
                uppercase = true;
            } else if uppercase {
                result.push_str(&c.to_uppercase().to_string());
                uppercase = false;
            } else {
                result.push_str(&c.to_lowercase().to_string());
                uppercase = true;
            }
        }

        result
    }

    fn to_reverse_alternating_case(&self) -> String {
        let mut result = String::new();
        let mut uppercase = false;

        for c in self.chars() {
            if c.is_whitespace() {
                result.push(c);
                uppercase = false;
            } else if uppercase {
                result.push_str(&c.to_uppercase().to_string());
                uppercase = false;
            } else {
                result.push_str(&c.to_lowercase().to_string());
                uppercase = true;
            }
        }

        result
    }
}
