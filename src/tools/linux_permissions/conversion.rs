/*
 * conversion.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

pub fn parse_from_boolean_arrays(permissions: &[bool; 9], special: &[bool; 3]) -> u16 {
    let mut mode: u16 = 0;

    // Set special bits
    if special[0] {
        mode |= 0o4000; // Set uid
    }
    if special[1] {
        mode |= 0o2000; // Set gid
    }
    if special[2] {
        mode |= 0o1000; // Sticky
    }
    if permissions[0] {
        mode |= 0o0400; // Read owner
    }
    if permissions[1] {
        mode |= 0o0200; // Write owner
    }
    if permissions[2] {
        mode |= 0o0100; // Execute owner
    }
    if permissions[3] {
        mode |= 0o0040; // Read group
    }
    if permissions[4] {
        mode |= 0o0020; // Write group
    }
    if permissions[5] {
        mode |= 0o0010; // Execute group
    }
    if permissions[6] {
        mode |= 0o0004; // Read others
    }
    if permissions[7] {
        mode |= 0o0002; // Write others
    }
    if permissions[8] {
        mode |= 0o0001; // Execute others
    }

    mode
}

pub fn parse_from_symbolic(symbolic: &str) -> Option<u16> {
    if symbolic.len() != 9 {
        return None;
    }

    let mut permissions = [false; 9];
    let mut special = [false; 3];

    // Owner permissions
    permissions[0] = symbolic.chars().nth(0)? == 'r';
    permissions[1] = symbolic.chars().nth(1)? == 'w';
    match symbolic.chars().nth(2)? {
        'x' => permissions[2] = true,
        's' => {
            permissions[2] = true;
            special[0] = true;
        }
        'S' => special[0] = true,
        '-' => {}
        _ => return None,
    }

    // Group permissions
    permissions[3] = symbolic.chars().nth(3)? == 'r';
    permissions[4] = symbolic.chars().nth(4)? == 'w';
    match symbolic.chars().nth(5)? {
        'x' => permissions[5] = true,
        's' => {
            permissions[5] = true;
            special[1] = true;
        }
        'S' => special[1] = true,
        '-' => {}
        _ => return None,
    }

    // Others permissions
    permissions[6] = symbolic.chars().nth(6)? == 'r';
    permissions[7] = symbolic.chars().nth(7)? == 'w';
    match symbolic.chars().nth(8)? {
        'x' => permissions[8] = true,
        't' => {
            permissions[8] = true;
            special[2] = true;
        }
        'T' => special[2] = true,
        '-' => {}
        _ => return None,
    }

    Some(parse_from_boolean_arrays(&permissions, &special))
}

pub fn to_boolean_array(mode: u16) -> ([bool; 9], [bool; 3]) {
    let mut permissions = [false; 9];
    let mut special = [false; 3];

    // Check special bits
    special[0] = (mode & 0o4000) != 0; // Set uid
    special[1] = (mode & 0o2000) != 0; // Set gid
    special[2] = (mode & 0o1000) != 0; // Sticky

    permissions[0] = (mode & 0o0400) != 0; // Read owner
    permissions[1] = (mode & 0o0200) != 0; // Write owner
    permissions[2] = (mode & 0o0100) != 0; // Execute owner
    permissions[3] = (mode & 0o0040) != 0; // Read group
    permissions[4] = (mode & 0o0020) != 0; // Write group
    permissions[5] = (mode & 0o0010) != 0; // Execute group
    permissions[6] = (mode & 0o0004) != 0; // Read others
    permissions[7] = (mode & 0o0002) != 0; // Write others
    permissions[8] = (mode & 0o0001) != 0; // Execute others

    (permissions, special)
}

pub fn numeric_to_symbolic(mode: u16) -> String {
    let (permissions, special) = to_boolean_array(mode);
    let mut symbolic = String::new();

    // Owner permissions
    symbolic.push(if permissions[0] { 'r' } else { '-' });
    symbolic.push(if permissions[1] { 'w' } else { '-' });
    if special[0] {
        symbolic.push(if permissions[2] { 's' } else { 'S' });
    } else {
        symbolic.push(if permissions[2] { 'x' } else { '-' });
    }

    // Group permissions
    symbolic.push(if permissions[3] { 'r' } else { '-' });
    symbolic.push(if permissions[4] { 'w' } else { '-' });
    if special[1] {
        symbolic.push(if permissions[5] { 's' } else { 'S' });
    } else {
        symbolic.push(if permissions[5] { 'x' } else { '-' });
    }

    // Others permissions
    symbolic.push(if permissions[6] { 'r' } else { '-' });
    symbolic.push(if permissions[7] { 'w' } else { '-' });
    if special[2] {
        symbolic.push(if permissions[8] { 't' } else { 'T' });
    } else {
        symbolic.push(if permissions[8] { 'x' } else { '-' });
    }

    symbolic
}
