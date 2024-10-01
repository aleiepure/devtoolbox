# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gdk


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/contrast_checker.ui')
class ContrastCheckerView(Adw.Bin):
    __gtype_name__ = "ContrastCheckerView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _label_color_btn = Gtk.Template.Child()
    _background_color_btn = Gtk.Template.Child()
    _example_box = Gtk.Template.Child()
    _example_title_lbl = Gtk.Template.Child()
    _example_lbl = Gtk.Template.Child()
    _aa_small_image = Gtk.Template.Child()
    _aa_large_image = Gtk.Template.Child()
    _aaa_small_image = Gtk.Template.Child()
    _aaa_large_image = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._set_example()
        self._check_wcag()

        # Signals
        self._background_color_btn.connect("notify::rgba", self._on_color_changed)
        self._label_color_btn.connect("notify::rgba", self._on_color_changed)

    def _on_color_changed(self, pspec: GObject.ParamSpec, user_data:GObject.GPointer):
        self._set_example()
        self._check_wcag()

    def _set_example(self):
        lbl_color = self._label_color_btn.get_rgba()
        bg_color = self._background_color_btn.get_rgba()

        lbl_css_str = "* { color: " + lbl_color.to_string() + "; }"
        bg_css_str = "* { background-color: " + bg_color.to_string() + "; }"

        lbl_css_provider = Gtk.CssProvider()

        # In GTK 4.8, bytes are expected, in GTK 4.10, you can provider a string, with a length.
        # This patch still allows bytes for backwards compatibility, and add support for
        # strings in GTK 4.8 and before.
        # https://gitlab.gnome.org/GNOME/pygobject/-/merge_requests/231
        # Credits to https://gitlab.gnome.org/amolenaar for the patch
        if (Gtk.get_major_version(), Gtk.get_minor_version()) >= (4, 9):
            lbl_css_provider.load_from_data(lbl_css_str, -1)
        else:
            lbl_css_provider.load_from_data(lbl_css_str.encode("utf-8"))

        self._example_title_lbl.get_style_context().add_provider(lbl_css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self._example_lbl.get_style_context().add_provider(lbl_css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        bg_css_provider = Gtk.CssProvider()

        # In GTK 4.8, bytes are expected, in GTK 4.10, you can provider a string, with a length.
        # This patch still allows bytes for backwards compatibility, and add support for
        # strings in GTK 4.8 and before.
        # https://gitlab.gnome.org/GNOME/pygobject/-/merge_requests/231
        # Credits to https://gitlab.gnome.org/amolenaar for the patch
        if (Gtk.get_major_version(), Gtk.get_minor_version()) >= (4, 9):
            bg_css_provider.load_from_data(bg_css_str, -1)
        else:
            bg_css_provider.load_from_data(bg_css_str.encode("utf-8"))
        self._example_box.get_style_context().add_provider(bg_css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _check_wcag(self):
        text_luminence = self._calculate_luminence(self._label_color_btn.get_rgba())
        background_luminence = self._calculate_luminence(self._background_color_btn.get_rgba())

        if text_luminence > background_luminence:
            contrast_ratio = (background_luminence + 0.05) / (text_luminence + 0.05)
        else:
            contrast_ratio = (text_luminence + 0.05) / (background_luminence + 0.05)

        aa_large = contrast_ratio < 1/3.0
        aa_small = contrast_ratio < 1/4.5
        aaa_large = contrast_ratio < 1/4.5
        aaa_small = contrast_ratio < 1/7.0

        if aa_large:
            self._aa_large_image.set_from_icon_name("check-round-outline")
            self._aa_large_image.remove_css_class("error")
            self._aa_large_image.add_css_class("success")
        else:
            self._aa_large_image.set_from_icon_name("error")
            self._aa_large_image.remove_css_class("success")
            self._aa_large_image.add_css_class("error")

        if aa_small:
            self._aa_small_image.set_from_icon_name("check-round-outline")
            self._aa_small_image.remove_css_class("error")
            self._aa_small_image.add_css_class("success")
        else:
            self._aa_small_image.set_from_icon_name("error")
            self._aa_small_image.remove_css_class("success")
            self._aa_small_image.add_css_class("error")

        if aaa_large:
            self._aaa_large_image.set_from_icon_name("check-round-outline")
            self._aaa_large_image.remove_css_class("error")
            self._aaa_large_image.add_css_class("success")
        else:
            self._aaa_large_image.set_from_icon_name("error")
            self._aaa_large_image.remove_css_class("success")
            self._aaa_large_image.add_css_class("error")

        if aaa_small:
            self._aaa_small_image.set_from_icon_name("check-round-outline")
            self._aaa_small_image.remove_css_class("error")
            self._aaa_small_image.add_css_class("success")
        else:
            self._aaa_small_image.set_from_icon_name("error")
            self._aaa_small_image.remove_css_class("success")
            self._aaa_small_image.add_css_class("error")


    def _calculate_luminence(self, color:Gdk.RGBA):
        r = self._luminence(color.red)
        g = self._luminence(color.green)
        b = self._luminence(color.blue)
        return r * 0.2126 + g * 0.7152 + b * 0.0722

    def _luminence(self, value:float):
        if value < 0.03928:
            return value/12.92
        else:
            return ((value+0.055)/1.055) ** 2.4
