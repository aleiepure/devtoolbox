/*
 * Copyright (C) 2022 - 2023 Alessandro Iepure
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

document.addEventListener("DOMContentLoaded", function (event) {
    var scrollpos = sessionStorage.getItem('scrollpos');
    if (scrollpos) {
        window.scrollTo(0, scrollpos);
        sessionStorage.removeItem('scrollpos');
    }
});

window.addEventListener("beforeunload", function (e) {
    sessionStorage.setItem('scrollpos', window.scrollY);
});
