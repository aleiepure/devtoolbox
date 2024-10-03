import base64
from gi.repository import Gio, GObject


class Base64EncoderService:

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _encode_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._encode(self._input)
        task.return_value(outcome)

    def _decode_thread(self, task: Gio.Task, source_object: GObject.Object, task_data: object, cancelable: Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._decode(self._input)
        task.return_value(outcome)

    def _encode(self, input: str) -> str:
        return base64.b64encode(input.encode()).decode()

    def _decode(self, input: str) -> str:
        return base64.b64decode(input.encode()).decode()

    def encode_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._encode_thread)

    def decode_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._decode_thread)

    def async_finish(self, result: Gio.AsyncResult, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._input = None
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input(self, input_str: str):
        self._input = input_str
