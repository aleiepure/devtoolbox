# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gio, GObject, Gdk
from gettext import gettext as _
from typing import List
from datetime import date
import re


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/views/reverse_cron.ui')
class ReverseCronView(Adw.Bin):
    __gtype_name__ = "ReverseCronView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _expand_btn = Gtk.Template.Child()

    _minutes_expander = Gtk.Template.Child()
    _minutes_every_btn = Gtk.Template.Child()
    _minutes_every_x_btn = Gtk.Template.Child()
    _minutes_every_x_dropdown = Gtk.Template.Child()
    _minutes_every_x_starting_dropdown = Gtk.Template.Child()
    _minutes_specific_btn = Gtk.Template.Child()
    _minutes_specific_grid = Gtk.Template.Child()
    _minutes_range_btn = Gtk.Template.Child()
    _minutes_range_x_dropdown = Gtk.Template.Child()
    _minutes_range_y_dropdown = Gtk.Template.Child()

    _hours_expander = Gtk.Template.Child()
    _hours_every_btn = Gtk.Template.Child()
    _hours_every_x_btn = Gtk.Template.Child()
    _hours_every_x_dropdown = Gtk.Template.Child()
    _hours_every_x_starting_dropdown = Gtk.Template.Child()
    _hours_specific_btn = Gtk.Template.Child()
    _hours_specific_grid = Gtk.Template.Child()
    _hours_range_btn = Gtk.Template.Child()
    _hours_range_x_dropdown = Gtk.Template.Child()
    _hours_range_y_dropdown = Gtk.Template.Child()

    _day_expander = Gtk.Template.Child()
    _day_every_btn = Gtk.Template.Child()
    _day_every_x_btn = Gtk.Template.Child()
    _day_every_x_dropdown = Gtk.Template.Child()
    _day_every_x_starting_dropdown = Gtk.Template.Child()
    _day_specific_btn = Gtk.Template.Child()
    _day_specific_grid = Gtk.Template.Child()
    _day_range_btn = Gtk.Template.Child()
    _day_range_x_dropdown = Gtk.Template.Child()
    _day_range_y_dropdown = Gtk.Template.Child()

    _month_expander = Gtk.Template.Child()
    _month_every_btn = Gtk.Template.Child()
    _month_every_x_btn = Gtk.Template.Child()
    _month_every_x_dropdown = Gtk.Template.Child()
    _month_every_x_starting_dropdown = Gtk.Template.Child()
    _month_specific_btn = Gtk.Template.Child()
    _month_specific_grid = Gtk.Template.Child()
    _month_range_btn = Gtk.Template.Child()
    _month_range_x_dropdown = Gtk.Template.Child()
    _month_range_y_dropdown = Gtk.Template.Child()

    _week_expander = Gtk.Template.Child()
    _week_every_btn = Gtk.Template.Child()
    _week_every_x_btn = Gtk.Template.Child()
    _week_every_x_dropdown = Gtk.Template.Child()
    _week_every_x_starting_dropdown = Gtk.Template.Child()
    _week_specific_btn = Gtk.Template.Child()
    _week_specific_grid = Gtk.Template.Child()
    _week_range_btn = Gtk.Template.Child()
    _week_range_x_dropdown = Gtk.Template.Child()
    _week_range_y_dropdown = Gtk.Template.Child()

    _command_row = Gtk.Template.Child()
    _cron_expression_row = Gtk.Template.Child()

    # Variables
    _is_expanded = False
    _minutes = "*"
    _hours = "*"
    _day = "*"
    _month = "*"
    _weekday = "*"

    def __init__(self):
        super().__init__()

        # Disable click effect inside expanders
        self._minutes_expander.get_child().get_last_child().get_first_child().get_first_child().remove_css_class("activatable")
        self._hours_expander.get_child().get_last_child().get_first_child().get_first_child().remove_css_class("activatable")
        self._day_expander.get_child().get_last_child().get_first_child().get_first_child().remove_css_class("activatable")
        self._month_expander.get_child().get_last_child().get_first_child().get_first_child().remove_css_class("activatable")
        self._week_expander.get_child().get_last_child().get_first_child().get_first_child().remove_css_class("activatable")

        # Fill drop-downs
        self._minutes_every_x_dropdown.set_model(self._get_bounded_model(1, 60))
        self._minutes_every_x_starting_dropdown.set_model(self._get_bounded_model(0, 59, leading_zero=True))
        self._minutes_range_x_dropdown.set_model(self._get_bounded_model(0, 59, leading_zero=True))
        self._minutes_range_y_dropdown.set_model(self._get_bounded_model(0, 59, leading_zero=True))
        self._hours_every_x_dropdown.set_model(self._get_bounded_model(1, 24))
        self._hours_every_x_starting_dropdown.set_model(self._get_bounded_model(0, 23, leading_zero=True))
        self._hours_range_x_dropdown.set_model(self._get_bounded_model(0, 23, leading_zero=True))
        self._hours_range_y_dropdown.set_model(self._get_bounded_model(0, 23, leading_zero=True))
        self._day_every_x_dropdown.set_model(self._get_bounded_model(1, 31))
        self._day_every_x_starting_dropdown.set_model(self._get_bounded_model(1, 31, day=True))
        self._day_range_x_dropdown.set_model(self._get_bounded_model(1, 31, day=True))
        self._day_range_y_dropdown.set_model(self._get_bounded_model(1, 31, day=True))
        self._month_every_x_dropdown.set_model(self._get_bounded_model(1, 12))
        self._week_every_x_dropdown.set_model(self._get_bounded_model(1, 7))

        # Fill grids
        self._fill_grid(self._minutes_specific_grid, 60)
        self._fill_grid(self._hours_specific_grid, 24)
        self._fill_grid(self._day_specific_grid, 31, include_zero=False)
        self._fill_month_grid()

        # Signals
        self._expand_btn.connect("clicked", self._on_expand_btn_clicked)
        self._command_row.connect("changed", self._on_command_changed)

        self._minutes_every_btn.connect("toggled", self._on_check_btn_toggled)
        self._minutes_every_x_btn.connect("toggled", self._on_check_btn_toggled)
        self._minutes_specific_btn.connect("toggled", self._on_check_btn_toggled)
        self._minutes_range_btn.connect("toggled", self._on_check_btn_toggled)
        self._minutes_every_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._minutes_every_x_starting_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._minutes_range_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._minutes_range_y_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._add_signals_in_grid(self._minutes_specific_grid, self._on_check_btn_toggled)

        self._hours_every_btn.connect("toggled", self._on_check_btn_toggled)
        self._hours_every_x_btn.connect("toggled", self._on_check_btn_toggled)
        self._hours_specific_btn.connect("toggled", self._on_check_btn_toggled)
        self._hours_range_btn.connect("toggled", self._on_check_btn_toggled)
        self._hours_every_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._hours_every_x_starting_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._hours_range_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._hours_range_y_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._add_signals_in_grid(self._hours_specific_grid, self._on_check_btn_toggled)

        self._day_every_btn.connect("toggled", self._on_check_btn_toggled)
        self._day_every_x_btn.connect("toggled", self._on_check_btn_toggled)
        self._day_specific_btn.connect("toggled", self._on_check_btn_toggled)
        self._day_range_btn.connect("toggled", self._on_check_btn_toggled)
        self._day_every_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._day_every_x_starting_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._day_range_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._day_range_y_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._add_signals_in_grid(self._day_specific_grid, self._on_check_btn_toggled)

        self._month_every_btn.connect("toggled", self._on_check_btn_toggled)
        self._month_every_x_btn.connect("toggled", self._on_check_btn_toggled)
        self._month_specific_btn.connect("toggled", self._on_check_btn_toggled)
        self._month_range_btn.connect("toggled", self._on_check_btn_toggled)
        self._month_every_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._month_every_x_starting_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._month_range_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._month_range_y_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._add_signals_in_grid(self._month_specific_grid, self._on_check_btn_toggled)

        self._week_every_btn.connect("toggled", self._on_check_btn_toggled)
        self._week_every_x_btn.connect("toggled", self._on_check_btn_toggled)
        self._week_specific_btn.connect("toggled", self._on_check_btn_toggled)
        self._week_range_btn.connect("toggled", self._on_check_btn_toggled)
        self._week_every_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._week_every_x_starting_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._week_range_x_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._week_range_y_dropdown.connect("notify::selected", self._on_dropdown_selected)
        self._add_signals_in_grid(self._week_specific_grid, self._on_check_btn_toggled)

        # First value
        self._get_cron()

    def _on_expand_btn_clicked(self, user_data:GObject.GPointer):

        # Swap button labels
        if self._is_expanded:
            self._expand_btn.get_child().set_label(_("Expand All"))
            self._expand_btn.get_child().set_icon_name("down-symbolic")
            self._is_expanded = False
        else:
            self._expand_btn.get_child().set_label(_("Collapse All"))
            self._expand_btn.get_child().set_icon_name("up-symbolic")
            self._is_expanded = True

        # Expand/collapse expanders
        self._minutes_expander.set_expanded(self._is_expanded)
        self._hours_expander.set_expanded(self._is_expanded)
        self._day_expander.set_expanded(self._is_expanded)
        self._month_expander.set_expanded(self._is_expanded)
        self._week_expander.set_expanded(self._is_expanded)

    def _on_dropdown_selected(self, pspec: GObject.ParamSpec, user_data: GObject.GPointer):
        self._get_cron()

    def _get_bounded_model(self, start: int, end: int, leading_zero: bool=False, day: bool=False) -> Gtk.StringList:
        output = Gtk.StringList()
        for i in range(start, end+1):
            if leading_zero:
                output.append(f"{i:02d}")
            else:
                if day:
                    if i == 1 or i == 21 or i == 31:
                        # TRANSLATORS: cardinal suffix for numbers
                        suffix = _("st")
                    elif i == 2 or i == 22:
                        # TRANSLATORS: cardinal suffix for numbers
                        suffix = _("nd")
                    elif i == 3 or i == 23:
                        # TRANSLATORS: cardinal suffix for numbers
                        suffix = _("rd")
                    else:
                        # TRANSLATORS: cardinal suffix for numbers
                        suffix = _("th")
                    output.append("%(day)s%(suffix)s" % {'day': i, 'suffix':suffix})
                else:
                    output.append(str(i))
        return output

    def _fill_grid(self, grid: Gtk.Grid, amount: int, include_zero :bool=True, start: int=0):
        if include_zero:
            for i in range(start, amount):
                check_btn = Gtk.CheckButton(label=f"{i:02d}")
                grid.attach(check_btn, i % 10, i / 10, 1, 1)
        else:
            start += 1
            for i in range(start, amount+1):
                check_btn = Gtk.CheckButton(label=f"{i:02d}")
                if i % 10 == 0 and not i == i * 10:
                    column = (i % 10) - 1
                elif i % 10 == 0 and i == i * 10:
                    column = (i * 10) - 1
                else:
                    column = (i % 10) - 1
                grid.attach(check_btn, column, i/10+1, 1, 1) # column, row, width, height

    def _fill_month_grid(self):
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("January")), 0, 0, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("February")), 1, 0, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("March")), 2, 0, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("April")), 3, 0, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("May")), 4, 0, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("June")), 5, 0, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("July")), 0, 1, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("August")), 1, 1, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("September")), 2, 1, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("October")), 3, 1, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("November")), 4, 1, 1, 1)
        self._month_specific_grid.attach(Gtk.CheckButton(label=_("December")), 5, 1, 1, 1)

    def _on_command_changed(self, user_data: GObject.GPointer):
        self._get_cron()

    def _add_signals_in_grid(self, grid: Gtk.Grid, callback: callable):
        widget = grid.get_first_child()
        if widget != None:
            widget.connect("toggled", callback)
            next_widget = widget.get_next_sibling()
            while next_widget != None:
                next_widget.connect("toggled", callback)
                widget = next_widget
                next_widget = widget.get_next_sibling()

    def _get_active_in_grid(self, grid: Gtk.Grid) -> List[str]:
        active_check_btns = []
        widget = grid.get_first_child()
        if widget != None:
            if widget.get_active():
                active_check_btns.append(widget)
            next_widget = widget.get_next_sibling()
            while next_widget != None:
                if next_widget.get_active():
                    active_check_btns.append(next_widget)
                widget = next_widget
                next_widget = widget.get_next_sibling()
        return active_check_btns

    def _on_check_btn_toggled(self, user_data: GObject.GPointer):
        self._get_cron()

    def _get_cron(self):

        # Minutes
        if self._minutes_every_btn.get_active():
            self._minutes = "*"
        if self._minutes_every_x_btn.get_active():
            self._minutes = f"{self._minutes_every_x_starting_dropdown.get_selected_item().get_string()}/{self._minutes_every_x_dropdown.get_selected_item().get_string()}"
        if self._minutes_specific_btn.get_active():
            self._minutes = ""
            active_btns = self._get_active_in_grid(self._minutes_specific_grid)
            if len(active_btns) == 0:
                self._minutes = "*"
            else:
                for btn in active_btns:
                    self._minutes += btn.get_label() + ","
                self._minutes = self._minutes[:-1]
        if self._minutes_range_btn.get_active():
            self._minutes = f"{self._minutes_range_x_dropdown.get_selected_item().get_string()}-{self._minutes_range_y_dropdown.get_selected_item().get_string()}"

        # Hours
        if self._hours_every_btn.get_active():
            self._hours = "*"
        if self._hours_every_x_btn.get_active():
            self._hours = f"{self._hours_every_x_starting_dropdown.get_selected_item().get_string()}/{self._hours_every_x_dropdown.get_selected_item().get_string()}"
        if self._hours_specific_btn.get_active():
            self._hours = ""
            active_btns = self._get_active_in_grid(self._hours_specific_grid)
            if len(active_btns) == 0:
                self._hours = "*"
            else:
                for btn in active_btns:
                    self._hours += btn.get_label() + ","
                self._hours = self._hours[:-1]
        if self._hours_range_btn.get_active():
            self._hours = f"{self._hours_range_x_dropdown.get_selected_item().get_string()}-{self._hours_range_y_dropdown.get_selected_item().get_string()}"

        # Day
        if self._day_every_btn.get_active():
            self._day = "*"
        if self._day_every_x_btn.get_active():
            starting_day = re.sub("\D", "", self._day_every_x_starting_dropdown.get_selected_item().get_string())
            interval = re.sub("\D", "", self._day_every_x_dropdown.get_selected_item().get_string())
            self._day = f"{starting_day}/{interval}"
        if self._day_specific_btn.get_active():
            self._day = ""
            active_btns = self._get_active_in_grid(self._day_specific_grid)
            if len(active_btns) == 0:
                self._day = "*"
            else:
                for btn in active_btns:
                    self._day += btn.get_label() + ","
                self._day = self._day[:-1]
        if self._day_range_btn.get_active():
            x = re.sub("\D", "", self._day_range_x_dropdown.get_selected_item().get_string())
            y = re.sub("\D", "", self._day_range_y_dropdown.get_selected_item().get_string())
            self._day = f"{x}-{y}"

        # Month
        if self._month_every_btn.get_active():
            self._month = "*"
        if self._month_every_x_btn.get_active():
            starting_month = self._month_every_x_starting_dropdown.get_selected() + 1
            interval = self._month_every_x_dropdown.get_selected_item().get_string()
            self._month = f"{starting_month}/{interval}"
        if self._month_specific_btn.get_active():
            self._month = ""
            active_btns = self._get_active_in_grid(self._month_specific_grid)
            if len(active_btns) == 0:
                self._month = "*"
            else:
                months = {
                    _("January"): 1,
                    _("February"): 2,
                    _("March"): 3,
                    _("April"): 4,
                    _("May"): 5,
                    _("June"): 6,
                    _("July"): 7,
                    _("August"): 8,
                    _("September"): 9,
                    _("October"): 10,
                    _("November"): 11,
                    _("December"): 12
                }
                for btn in active_btns:
                    self._month += str(months[btn.get_label()]) + ","
                self._month = self._month[:-1]
        if self._month_range_btn.get_active():
            x = self._month_range_x_dropdown.get_selected() + 1
            y = self._month_range_y_dropdown.get_selected() + 1
            self._month = f"{x}-{y}"

        weekdays = {
            _("Sunday"): 0,
            _("Monday"): 1,
            _("Tuesday"): 2,
            _("Wednesday"): 3,
            _("Thursday"): 4,
            _("Friday"): 5,
            _("Saturday"): 6,
        }
        if self._week_every_btn.get_active():
            self._weekday = "*"
        if self._week_every_x_btn.get_active():
            starting_weekday = self._week_every_x_starting_dropdown.get_selected_item().get_string()
            interval = self._week_every_x_dropdown.get_selected_item().get_string()
            self._weekday = f"{weekdays[starting_weekday]}/{interval}"
        if self._week_specific_btn.get_active():
            self._weekday = ""
            active_btns = self._get_active_in_grid(self._week_specific_grid)
            if len(active_btns) == 0:
                self._weekday = "*"
            else:
                for btn in active_btns:
                    self._weekday += str(weekdays[btn.get_label()]) + ","
                self._weekday = self._weekday[:-1]
        if self._week_range_btn.get_active():
            x = self._week_range_x_dropdown.get_selected_item().get_string()
            y = self._week_range_y_dropdown.get_selected_item().get_string()
            self._weekday = f"{weekdays[x]}-{weekdays[y]}"

        self._cron_expression_row.set_text(self._minutes + " " + self._hours + " " + self._day + " " + self._month + " " + self._weekday + " " + self._command_row.get_text())
