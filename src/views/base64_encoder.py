from gi.repository import Gtk, Adw, Gio, GObject
from gettext import gettext as _

from ..services.base64_encoder import Base64EncoderService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/base64_encoder.ui")
class Base64EncoderView(Adw.Bin):
    __gtype_name__ = "Base64EncoderView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _direction_selector = Gtk.Template.Child()
    _url_safe_switch = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()

    _service = Base64EncoderService()

    def __init__(self):
        super().__init__()

        # Language highlight
        self._input_area.set_text_language_highlight("plain")  # Base64 input is typically plain text
        self._output_area.set_text_language_highlight("plain")

        # Signals
        # self._direction_selector.connect("toggled", self._on_input_changed)
        self._direction_selector.connect("notify::active", self._on_direction_changed)
        self._url_safe_switch.connect("notify::active", self._on_direction_changed)
        self._input_area.connect("text-changed", self._on_input_changed)
        self._input_area.connect("error", self._on_error)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._output_area.connect("error", self._on_error)

    def _on_direction_changed(self, pspec: GObject.ParamSpec, user_data: GObject.GPointer):
        self._convert()
        
    def _on_url_safe_changed(self, pspec: GObject.ParamSpec, user_data: GObject.GPointer):
        self._service.set_url_safe(self._url_safe_switch.get_active())
        self._convert()

    def _on_input_changed(self, source_widget: GObject.Object):
        self._convert()

    def _on_view_cleared(self, source_widget: GObject.Object):
        self._output_area.clear()

    def _on_error(self, source_widget: GObject.Object, error: str):
        self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(error=error), priority=Adw.ToastPriority.HIGH))

    def _convert(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        text = self._input_area.get_text()
        self._service.set_input(text)

        # Call task
        if self._direction_selector.get_active() == 0:  # True: encode, False: decode
            self._output_area.set_spinner_spin(True)
            self._service.encode_async(self, self._on_async_done)
        else:
            self._output_area.set_spinner_spin(True)
            self._service.decode_async(self, self._on_async_done)

    def _on_async_done(self, source_widget: GObject.Object, result: Gio.AsyncResult, user_data: GObject.GPointer):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.async_finish(result, self)
        self._output_area.set_text(outcome)
