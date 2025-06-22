from gi.repository import Gtk, Adw, Gio, Gdk
from gettext import gettext as _
from ..utils import Utils
import colorsys
from color_parser_py import ColorParser
from enum import IntEnum


class Format(IntEnum):
    WEB = 0
    WEB_LEGACY = 1
    PERCENT = 2
    NORMALIZED = 3
    NBIT = 4


class AngleUnit(IntEnum):
    DEG = 0
    RAD = 1
    GRAD = 2
    TURN = 3
    FOLLOW = 4


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/color_converter.ui")
class ColorConverterView(Adw.Bin):
    __gtype_name__ = "ColorConverterView"

    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()

    _color_btn = Gtk.Template.Child()
    _format_combo = Gtk.Template.Child()
    _angle_combo = Gtk.Template.Child()
    _bits_spinner = Gtk.Template.Child()
    _hex = Gtk.Template.Child()
    _rgb_row = Gtk.Template.Child()
    _rgb_red = Gtk.Template.Child()
    _rgb_green = Gtk.Template.Child()
    _rgb_blue = Gtk.Template.Child()
    _hsv_row = Gtk.Template.Child()
    _hsv_hue = Gtk.Template.Child()
    _hsv_sat = Gtk.Template.Child()
    _hsv_val = Gtk.Template.Child()
    _hsl_row = Gtk.Template.Child()
    _hsl_hue = Gtk.Template.Child()
    _hsl_sat = Gtk.Template.Child()
    _hsl_lit = Gtk.Template.Child()
    _alpha = Gtk.Template.Child()
    _rgb_web = Gtk.Template.Child()
    _hsl_web = Gtk.Template.Child()
    _hwb_web = Gtk.Template.Child()

    _invalid_toast = Adw.Toast(title=_("Invalid value. Please check again"))


    def __init__(self):
        super().__init__()

        self._settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

        # Current color
        self._color = Gdk.RGBA(*([1.0] * 4))

        # Signals
        self._format_combo_handler = self._format_combo.connect("notify::selected", self._on_format_combo)
        self._angle_combo_handler = self._angle_combo.connect("notify::selected", self._on_angle_combo)
        self._bits_spinner_handler = self._bits_spinner.connect("notify::value", self._on_bits_spinner)
        self._color_btn_handler = self._color_btn.connect("notify::rgba", self._on_color_btn)
        self._hex_handler = self._hex.connect("notify::text", self._on_hex_changed)
        self._rgb_web_handler = self._rgb_web.connect("notify::text", self._on_rgb_web_changed)
        self._hsl_web_handler = self._hsl_web.connect("notify::text", self._on_hsl_web_changed)
        self._hwb_web_handler = self._hwb_web.connect("notify::text", self._on_hwb_web_changed)
        self._rgb_red_handler = self._rgb_red.connect("notify::text", self._on_rgb_changed)
        self._rgb_green_handler = self._rgb_green.connect("notify::text", self._on_rgb_changed)
        self._rgb_blue_handler = self._rgb_blue.connect("notify::text", self._on_rgb_changed)
        self._hsv_hue_handler = self._hsv_hue.connect("notify::text", self._on_hsv_changed)
        self._hsv_sat_handler = self._hsv_sat.connect("notify::text", self._on_hsv_changed)
        self._hsv_val_handler = self._hsv_val.connect("notify::text", self._on_hsv_changed)
        self._hsl_hue_handler = self._hsl_hue.connect("notify::text", self._on_hsl_changed)
        self._hsl_sat_handler = self._hsl_sat.connect("notify::text", self._on_hsl_changed)
        self._hsl_lit_handler = self._hsl_lit.connect("notify::text", self._on_hsl_changed)
        self._alpha_handler = self._alpha.connect("notify::text", self._on_alpha_changed)

        # Restore Tool Settings
        stored_format = self._settings.get_int("color-converter-format")
        stored_angle = self._settings.get_int("color-converter-angle")
        stored_bits = self._settings.get_int("color-converter-bits")
        self._format_combo.set_selected(stored_format)
        self._angle_combo.set_selected(stored_angle)
        self._bits_spinner.set_value(stored_bits)

        self._update_all_visible()


    def _on_format_combo(self, *__):
        selected = self._format_combo.get_selected()
        self._settings.set_int("color-converter-format", selected)

        # Make relevant UI visible
        is_web = selected in (Format.WEB, Format.WEB_LEGACY)
        is_legacy = selected == Format.WEB_LEGACY
        self._rgb_web.set_visible(is_web)
        self._hsl_web.set_visible(is_web)
        self._hwb_web.set_visible(is_web and not is_legacy)
        self._rgb_row.set_visible(not is_web)
        self._hsv_row.set_visible(not is_web)
        self._hsl_row.set_visible(not is_web)
        self._alpha.set_visible(not is_web)
        self._angle_combo.set_visible(not is_web)
        self._bits_spinner.set_visible(selected == Format.NBIT)

        self._update_all_visible("color", "hex")


    def _on_angle_combo(self, *__):
        selected = self._angle_combo.get_selected()
        self._settings.set_int("color-converter-angle", selected)

        h, *__ = self._get_hsv()
        self._hsv_hue.handler_block(self._hsv_hue_handler)
        self._hsl_hue.handler_block(self._hsl_hue_handler)
        self._hsv_hue.set_text(self._format_angle(h))
        self._hsl_hue.set_text(self._format_angle(h))
        self._hsv_hue.handler_unblock(self._hsv_hue_handler)
        self._hsl_hue.handler_unblock(self._hsl_hue_handler)


    def _on_bits_spinner(self, *__):
        value = int(self._bits_spinner.get_value())
        self._settings.set_int("color-converter-bits", value)

        self._update_values()


    def _on_color_btn(self, *__):
        self._color = self._color_btn.get_rgba()
        self._update_all_visible("color")


    def _on_hex_changed(self, *__):
        self._parse_input(self._hex.get_text(), self._hex)
        self._update_all_visible("hex")


    def _on_rgb_web_changed(self, *__):
        self._parse_input(self._rgb_web.get_text(), self._rgb_web)
        self._update_all_visible("rgb")


    def _on_hsl_web_changed(self, *__):
        self._parse_input(self._hsl_web.get_text(), self._hsl_web)
        self._update_all_visible("hsl")


    def _on_hwb_web_changed(self, *__):
        self._parse_input(self._hwb_web.get_text(), self._hwb_web)
        self._update_all_visible("hwb")


    def _on_rgb_changed(self, *__):
        r = self._parse_number(self._rgb_red.get_text(), self._rgb_red)
        g = self._parse_number(self._rgb_green.get_text(), self._rgb_green)
        b = self._parse_number(self._rgb_blue.get_text(), self._rgb_blue)
        if None not in (r, g, b):
            self._color.red, self._color.green, self._color.blue = r, g, b
            self._invalid_toast.dismiss()
        self._update_all_visible("rgb", "alpha")


    def _on_hsv_changed(self, *__):
        h = self._parse_angle(self._hsv_hue.get_text(), self._hsv_hue)
        s = self._parse_number(self._hsv_sat.get_text(), self._hsv_sat)
        v = self._parse_number(self._hsv_val.get_text(), self._hsv_val)
        if None not in (h, s, v):
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            self._color.red, self._color.green, self._color.blue = r, g, b
            self._invalid_toast.dismiss()
        self._update_all_visible("hsv", "alpha")


    def _on_hsl_changed(self, *__):
        h = self._parse_angle(self._hsl_hue.get_text(), self._hsl_hue)
        s = self._parse_number(self._hsl_sat.get_text(), self._hsl_sat)
        l = self._parse_number(self._hsl_lit.get_text(), self._hsl_lit)
        if None not in (h, s, l):
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            self._color.red, self._color.green, self._color.blue = r, g, b
            self._invalid_toast.dismiss()
        self._update_all_visible("hsl", "alpha")


    def _on_alpha_changed(self, *__):
        alpha = self._parse_number(self._alpha.get_text(), self._alpha)
        if alpha is not None:
            self._color.alpha = alpha
            self._invalid_toast.dismiss()
        self._update_all_visible("alpha", "rgb", "hsv", "hsl")


    def _update_all_visible(self, *exclude):
        if "color" not in exclude:
            self._update_color_btn()
        if "hex" not in exclude:
            self._update_hex()

        match self._format_combo.get_selected():
            case Format.WEB:
                self._update_web(*exclude)
            case Format.WEB_LEGACY:
                self._update_web_legacy(*exclude)
            case _:
                self._update_values(*exclude)


    def _update_hex(self):
        parsed = ColorParser(f"rgba({Utils.normalized_to_uint8(self._color.red)}, "
                             f"{Utils.normalized_to_uint8(self._color.green)}, "
                             f"{Utils.normalized_to_uint8(self._color.blue)}, "
                             f"{Utils.format_decimal(self._color.alpha, 3)})")
        self._hex.handler_block(self._hex_handler)
        self._hex.set_text(parsed.hex)
        self._hex.remove_css_class("border-red")
        self._hex.handler_unblock(self._hex_handler)


    def _update_color_btn(self):
        self._color_btn.handler_block(self._color_btn_handler)
        self._color_btn.set_rgba(self._color)
        self._color_btn.handler_unblock(self._color_btn_handler)


    def _update_web(self, *exclude):
        if self._color.alpha < 1.0:
            alpha = f" / {Utils.format_decimal(Utils.normalized_to_percent(self._color.alpha))}%"
        else:
            alpha = ""

        if "rgb" not in exclude:
            red = Utils.format_decimal(Utils.normalized_to_percent(self._color.red))
            green = Utils.format_decimal(Utils.normalized_to_percent(self._color.green))
            blue = Utils.format_decimal(Utils.normalized_to_percent(self._color.blue))
            self._rgb_web.handler_block(self._rgb_web_handler)
            self._rgb_web.set_text(f"rgb({red}% {green}% {blue}%{alpha})")
            self._rgb_web.remove_css_class("border-red")
            self._rgb_web.handler_unblock(self._rgb_web_handler)
        if "hsl" not in exclude:
            h, s, l = self._get_hsl()
            hue = Utils.format_decimal(Utils.normalized_to_deg(h))
            sat = Utils.format_decimal(Utils.normalized_to_percent(s))
            lit = Utils.format_decimal(Utils.normalized_to_percent(l))
            self._hsl_web.handler_block(self._hsl_web_handler)
            self._hsl_web.set_text(f"hsl({hue} {sat}% {lit}%{alpha})")
            self._hsl_web.remove_css_class("border-red")
            self._hsl_web.handler_unblock(self._hsl_web_handler)
        if "hwb" not in exclude:
            h, w, b = self._get_hwb()
            hue = Utils.format_decimal(Utils.normalized_to_deg(h))
            whi = Utils.format_decimal(Utils.normalized_to_percent(w))
            bla = Utils.format_decimal(Utils.normalized_to_percent(b))
            self._hwb_web.handler_block(self._hwb_web_handler)
            self._hwb_web.set_text(f"hwb({hue} {whi}% {bla}%{alpha})")
            self._hwb_web.remove_css_class("border-red")
            self._hwb_web.handler_unblock(self._hwb_web_handler)


    def _update_web_legacy(self, *exclude):
        if "rgb" not in exclude:
            red = Utils.normalized_to_uint8(self._color.red)
            green = Utils.normalized_to_uint8(self._color.green)
            blue = Utils.normalized_to_uint8(self._color.blue)
            self._rgb_web.handler_block(self._rgb_web_handler)
            if self._color.alpha < 1.0:
                alpha = Utils.format_decimal(self._color.alpha, 3)
                self._rgb_web.set_text(f"rgba({red}, {green}, {blue}, {alpha})")
            else:
                self._rgb_web.set_text(f"rgb({red}, {green}, {blue})")
            self._rgb_web.remove_css_class("border-red")
            self._rgb_web.handler_unblock(self._rgb_web_handler)

        if "hsl" not in exclude:
            h, s, l = self._get_hsl()
            hue = round(Utils.normalized_to_deg(h))
            sat = round(Utils.normalized_to_percent(s))
            lit = round(Utils.normalized_to_percent(l))
            self._hsl_web.handler_block(self._hsl_web_handler)
            if self._color.alpha < 1.0:
                alpha = Utils.format_decimal(self._color.alpha, 3)
                self._hsl_web.set_text(f"hsla({hue}, {sat}%, {lit}%, {alpha})")
            else:
                self._hsl_web.set_text(f"hsl({hue}, {sat}%, {lit}%)")
            self._hsl_web.remove_css_class("border-red")
            self._hsl_web.handler_unblock(self._hsl_web_handler)


    def _update_values(self, *exclude):
        if "rgb" not in exclude:
            self._rgb_red.handler_block(self._rgb_red_handler)
            self._rgb_green.handler_block(self._rgb_green_handler)
            self._rgb_blue.handler_block(self._rgb_blue_handler)
            self._rgb_red.set_text(self._format_value(self._color.red))
            self._rgb_green.set_text(self._format_value(self._color.green))
            self._rgb_blue.set_text(self._format_value(self._color.blue))
            self._rgb_red.remove_css_class("border-red")
            self._rgb_green.remove_css_class("border-red")
            self._rgb_blue.remove_css_class("border-red")
            self._rgb_red.handler_unblock(self._rgb_red_handler)
            self._rgb_green.handler_unblock(self._rgb_green_handler)
            self._rgb_blue.handler_unblock(self._rgb_blue_handler)
        if "hsv" not in exclude:
            h, s, v = self._get_hsv()
            self._hsv_hue.handler_block(self._hsv_hue_handler)
            self._hsv_sat.handler_block(self._hsv_sat_handler)
            self._hsv_val.handler_block(self._hsv_val_handler)
            self._hsv_hue.set_text(self._format_angle(h))
            self._hsv_sat.set_text(self._format_value(s))
            self._hsv_val.set_text(self._format_value(v))
            self._hsv_hue.remove_css_class("border-red")
            self._hsv_sat.remove_css_class("border-red")
            self._hsv_val.remove_css_class("border-red")
            self._hsv_hue.handler_unblock(self._hsv_hue_handler)
            self._hsv_sat.handler_unblock(self._hsv_sat_handler)
            self._hsv_val.handler_unblock(self._hsv_val_handler)
        if "hsl" not in exclude:
            h, s, l = self._get_hsl()
            self._hsl_hue.handler_block(self._hsl_hue_handler)
            self._hsl_sat.handler_block(self._hsl_sat_handler)
            self._hsl_lit.handler_block(self._hsl_lit_handler)
            self._hsl_hue.set_text(self._format_angle(h))
            self._hsl_sat.set_text(self._format_value(s))
            self._hsl_lit.set_text(self._format_value(l))
            self._hsl_hue.remove_css_class("border-red")
            self._hsl_sat.remove_css_class("border-red")
            self._hsl_lit.remove_css_class("border-red")
            self._hsl_hue.handler_unblock(self._hsl_hue_handler)
            self._hsl_sat.handler_unblock(self._hsl_sat_handler)
            self._hsl_lit.handler_unblock(self._hsl_lit_handler)
        if "alpha" not in exclude:
            self._alpha.handler_block(self._alpha_handler)
            self._alpha.set_text(self._format_value(self._color.alpha))
            self._alpha.remove_css_class("border-red")
            self._alpha.handler_unblock(self._alpha_handler)


    def _parse_input(self, parsable, input_field):
        if ColorParser.is_valid(parsable):
            self._color = Gdk.RGBA(*ColorParser(parsable).rgba_float)
            input_field.remove_css_class("border-red")
            self._invalid_toast.dismiss()
        else:
            self._toast.add_toast(self._invalid_toast)
            input_field.add_css_class("border-red")


    def _parse_number(self, parsable, input_field) -> float | None:
        try:
            match self._format_combo.get_selected():
                case Format.NBIT:
                    parsed = Utils.uintn_to_normalized(int(parsable), int(self._bits_spinner.get_value()))
                case Format.PERCENT:
                    parsed = Utils.percent_to_normalized(float(parsable))
                case _:
                    parsed = float(parsable)
            if parsed is not None:
                input_field.remove_css_class("border-red")
            return parsed
        except ValueError:
            self._toast.add_toast(self._invalid_toast)
            input_field.add_css_class("border-red")
            return None


    def _parse_angle(self, parsable, input_field) -> float | None:
        try:
            match self._angle_combo.get_selected():
                case AngleUnit.DEG:
                    parsed = Utils.deg_to_normalized(float(parsable))
                case AngleUnit.RAD:
                    parsed = Utils.rad_to_normalized(float(parsable))
                case AngleUnit.GRAD:
                    parsed = Utils.grad_to_normalized(float(parsable))
                case AngleUnit.TURN:
                    parsed = float(parsable) % 1.0
                case _:
                    parsed = self._parse_number(parsable, input_field)
            if parsed is not None:
                input_field.remove_css_class("border-red")
            return parsed
        except ValueError:
            self._toast.add_toast(self._invalid_toast)
            input_field.add_css_class("border-red")
            return None


    def _format_value(self, value: float) -> str:
        match self._format_combo.get_selected():
            case Format.PERCENT:
                return Utils.format_decimal(Utils.normalized_to_percent(value))
            case Format.NBIT:
                return str(Utils.normalized_to_uintn(value, int(self._bits_spinner.get_value())))
            case _:
                return Utils.format_decimal(value, 4)


    def _format_angle(self, angle: float) -> str:
        match self._angle_combo.get_selected():
            case AngleUnit.DEG:
                return self._format_angle_int_dec(Utils.normalized_to_deg(angle))
            case AngleUnit.RAD:
                return Utils.format_decimal(Utils.normalized_to_rad(angle), 3)
            case AngleUnit.GRAD:
                return self._format_angle_int_dec(Utils.normalized_to_grad(angle))
            case AngleUnit.TURN:
                return Utils.format_decimal(angle, 4)
            case _:
                return self._format_value(angle)


    def _format_angle_int_dec(self, angle: float) -> str:
        if self._format_combo.get_selected() == Format.NBIT:
            return str(round(angle))
        else:
            return Utils.format_decimal(angle)


    def _get_hsv(self):
        hsv = colorsys.rgb_to_hsv(self._color.red, self._color.green, self._color.blue)
        return hsv[0], hsv[1], hsv[2]


    def _get_hsl(self):
        hls = colorsys.rgb_to_hls(self._color.red, self._color.green, self._color.blue)
        return hls[0], hls[2], hls[1]


    def _get_hwb(self):
        h, *_ = colorsys.rgb_to_hls(self._color.red, self._color.green, self._color.blue)
        w = min(self._color.red, self._color.green, self._color.blue)
        b = 1.0 - max(self._color.red, self._color.green, self._color.blue)
        return h, w, b

