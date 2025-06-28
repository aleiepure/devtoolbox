# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, GObject, Gio, Gdk, Gcr, GLib
from gettext import gettext as _
from typing import List

from ..services.certificate_parser import CertificateParserService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/certificate_parser.ui")
class CertificateParserView(Adw.Bin):
    __gtype_name__ = "CertificateParserView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _open_certificate_row = Gtk.Template.Child()
    _path_lbl = Gtk.Template.Child()
    _open_btn = Gtk.Template.Child()
    _view_stack = Gtk.Template.Child()
    _certificate_group = Gtk.Template.Child()
    _expand_btn = Gtk.Template.Child()
    _identity_lbl = Gtk.Template.Child()
    _verified_by_lbl = Gtk.Template.Child()
    _expire_lbl = Gtk.Template.Child()
    _general_group = Gtk.Template.Child()
    _named_extensions_group = Gtk.Template.Child()
    _extensions_group = Gtk.Template.Child()

    # Service
    _service = CertificateParserService()

    # Variables
    _general = []
    _extensions = []
    _named_extensions = []
    _is_expanded = False

    def __init__(self):
        super().__init__()

        # Drag and drop
        content = Gdk.ContentFormats.new_for_gtype(Gdk.FileList)
        target = Gtk.DropTarget(formats=content, actions=Gdk.DragAction.COPY)
        target.connect("drop", self._on_dnd_drop)
        self._open_certificate_row.add_controller(target)

        # Signals
        self._open_btn.connect("clicked", self._on_open_btn_clicked)
        self._path_lbl.connect("notify::label", self._on_file_opened)
        self._expand_btn.connect("clicked", self._on_expand_btn_clicked)

    def _on_dnd_drop(self, drop_target:Gtk.DropTarget, value: Gdk.FileList, x:float, y:float, user_data:GObject.Object=None):
        files: List[Gio.File] = value.get_files()

        # Error on multiple files
        if len(files) != 1:
            self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(error=_("Cannot open more than one file")), priority=Adw.ToastPriority.HIGH))
            return

        # Error on unsupported files
        if files[0].get_path()[-3:] not in ["cer", "der", "pem"]:
            self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(error=_("Unsupported file")), priority=Adw.ToastPriority.HIGH))
            return

        self._path_lbl.set_label(files[0].get_path())

    def _on_open_btn_clicked(self, user_data:GObject.GPointer):

        # Disable button
        self._open_btn.set_sensitive(False)
        self._open_certificate_row.remove_css_class("border-red")

        # Create a file chooser
        app = Gio.Application.get_default()
        window = app.get_active_window()
        self._file_dialog = Gtk.FileDialog(
            modal=True,
            title=_("Open File"),
            accept_label=_("Open"),
        )

        # Set filters
        file_filter = Gtk.FileFilter()
        file_filter.add_suffix("cer")
        file_filter.add_suffix("der")
        file_filter.add_suffix("pem")
        file_filter.set_name(_("Certificates"))
        
        filter_store = Gio.ListStore.new(Gtk.FileFilter)
        filter_store.append(file_filter)
        self._file_dialog.set_filters(filter_store)

        self._file_dialog.open(window, None, self._on_open_dialog_complete, None)

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
        for expander in self._general:
            expander.set_expanded(self._is_expanded)
        for expander in self._named_extensions:
            expander.set_expanded(self._is_expanded)
        for expander in self._extensions:
            expander.set_expanded(self._is_expanded)


    def _on_open_dialog_complete(self, source: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        try:
            file = source.open_finish(result)
            self._path_lbl.set_label(file.get_path())
        except GLib.GError:
            pass
        
        self._open_btn.set_sensitive(True)

    def _on_file_opened(self, source_widget:GObject.Object, user_data:GObject.GPointer):

        # Empty groups
        self._empty_groups()

        # Setup task
        self._service.set_path(self._path_lbl.get_label())
        self._service.get_gcr_async(self, self._on_gcr_done)

    def _on_gcr_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):

        # Get certificate object
        certificate = self._service.get_gcr_async_finish(result, self)

        elements = certificate.get_interface_elements()
        if not elements:
            self._open_certificate_row.add_css_class("border-red")
            self._toast.add_toast(Adw.Toast(title=_("Error: Cannot open this file because it is not a valid certificate."), priority=Adw.ToastPriority.HIGH))
            self._view_stack.set_visible_child_name("empty")
            return

        # General sections
        self._certificate_group.set_title(elements[0].get_label())

        # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
        self._identity_lbl.set_label(_("Identity: {identity}").format(identity=str(elements[0].get_fields()[0].get_property("value"))))
        # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
        self._verified_by_lbl.set_label(_("Verified by: {verified_by}").format(verified_by=str(elements[0].get_fields()[1].get_property("value"))))
        # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
        self._expire_lbl.set_label(_("Expires: {expiration_date}").format(expiration_date=str(elements[0].get_fields()[2].get_property("value"))))

        # Extensions
        for i in range(2, len(elements)):

            # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
            if elements[i].get_label() in [_("Basic Constraints"),          # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
                                           _("Extended Key Usage"),         # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
                                           _("Subject Key Identifier"),     # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
                                           _("Key Usage"),                  # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
                                           _("Subject Alternative Names")]:
                self._named_extensions.append(self._create_expander(elements[i].get_label(), elements[i].get_fields()))

            # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
            elif elements[i].get_label() == _("Extension"):
                self._extensions.append(self._create_expander(elements[i].get_label(), elements[i].get_fields()))

            else:
                self._general.append(self._create_expander(elements[i].get_label(), elements[i].get_fields()))

        # Fill groups and show view (hide "open certificate")
        for row in self._general:
            self._general_group.add(row)
        for row in self._extensions:
            self._extensions_group.add(row)
        for row in self._named_extensions:
            self._named_extensions_group.add(row)

        self._view_stack.set_visible_child_name("certificate")

    def _create_expander(self, title:str, fields:List[Gcr.CertificateField]) -> Adw.ExpanderRow:
        expander = Adw.ExpanderRow(title=title)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                      spacing=6,
                      margin_top=6,
                      margin_bottom=6,
                      margin_start=12)

        # Convert fields to strings based on their content
        for field in fields:

            # bytes: format as hex string
            if type(field.get_property("value")) == GLib.Bytes:
                value = self._format_hex_data(field.get_property("value").get_data().hex().upper(), 10, field.get_label())

            # list: format as comma separated string
            elif type(field.get_property("value")) == list:
                value = ""
                for item in field.get_property("value"):
                    value += item + ",\n" + self._calculate_indent_string(field.get_label())
                value = value[:len(value)-2-len(self._calculate_indent_string(field.get_label()))]

            # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
            elif field.get_section().get_label() in [_("Subject Key Identifier"),       # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
                                                     _("Certificate Fingerprints")]:

                # TRANSLATORS: MUST use the same translations from https://gitlab.gnome.org/GNOME/gcr/-/tree/4.1.0/po
                if field.get_label() in [_("Key Identifier"), "SHA1", "MD5"]:
                    value = self._format_sting_hex(str(field.get_property("value")), field.get_label())
                else:
                    value = str(field.get_property("value"))

            # plain string
            else:
                value = str(field.get_property("value"))

            label = Gtk.Label(label=field.get_label() + ": " + value, halign=Gtk.Align.START, css_classes=["monospace"], selectable=True)
            box.append(label)

        expander.add_row(box)

        # Disable hover effect
        expander.get_child().get_last_child().get_first_child().get_first_child().remove_css_class("activatable")

        # Set expander status
        expander.set_expanded(self._is_expanded)

        return expander

    def _format_hex_data(self, data:str, num:int, label:str) -> str:
        output = ""

        # Break string in pieces
        pieces_list = [data[i:i + 2] for i in range(0, len(data), 2)]

        # Divide pieces list in groups
        pieces_group = [pieces_list[x:x+num] for x in range(0, len(pieces_list), num)]

        # Format string
        for group in pieces_group:
            for piece in group:
                output += piece + " "
            output += "\n" + self._calculate_indent_string(label)

        # Return string without end white-spaces
        return output[:-len(self._calculate_indent_string(label))-2]

    def _format_sting_hex(self, value:str, label:str):

        # Some segments have hex data already formatted as strings, format them as
        # other hex values

        value = value.replace(" ", "").upper()
        return self._format_hex_data(value, 10, label)

    def _calculate_indent_string(self, label:str) -> str:
        output = ""
        for i in range(0, len(label)+2):
            output += " "
        return output

    def _empty_groups(self):
        for row in self._general:
            self._general_group.remove(row)
        self._general = []

        for row in self._extensions:
            self._extensions_group.remove(row)
        self._extensions = []

        for row in self._named_extensions:
            self._named_extensions_group.remove(row)
        self._named_extensions = []
