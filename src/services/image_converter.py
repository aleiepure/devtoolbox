# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from PIL import Image


class ImageConverterService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_file(self, file:Gio.File):
        self._file = file

    def set_destination_format(self, destination_format:int):
        self._destination_format = destination_format

    def set_destination_file(self, destination_file:Gio.File):
        self._destination_file = destination_file

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._file = None
        self._destination_format = None
        self._destination_file = None
        return result.propagate_value().value

    def convert_image_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_image_thread)

    def _convert_image_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_image(self._file, self._destination_format, self._destination_file)
        task.return_value(outcome)

    def _convert_image(self, file:Gio.File, destination_format:int, destination_file:Gio.File):

        img = Image.open(file.get_path())

        match destination_format:
            case 0: # BMP
                extension = "bmp"
            case 1: # GIF
                extension = "gif"
            case 2: # ICNS
                extension = "icns"
            case 3: # JPEG
                extension = "jpeg"
                img = img.convert('RGB')
            case 4: # PNG
                extension = "png"
            case 5: # TIFF
                extension = "tiff"
            case 6: # WEBP
                extension = "webp"

        img.save(destination_file.get_path(), format=extension)
        return destination_file.get_path()
