# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from daltonlens import convert, simulate
from PIL import Image
import numpy as np


class ColorblindnessSimulatorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()
        self._protanopia_file = Gio.File.new_tmp("me.iepure.devtoolbox.XXXXXX.png")[0]
        self._deutranopia_file = Gio.File.new_tmp("me.iepure.devtoolbox.XXXXXX.png")[0]
        self._tritanopia_file = Gio.File.new_tmp("me.iepure.devtoolbox.XXXXXX.png")[0]

    def set_original_file(self, file:Gio.File):
        self._original_file = file

    def set_severity(self, severity:float):
        self._severity = severity

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result, caller: GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._original_file = None
        return result.propagate_value().value

    def simulate_async(self, caller: GObject.Object, callback: callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._simulate_thread)

    def _simulate_thread(self, task, source_object, task_data, cancelable):
        if task.return_error_if_cancelled():
            return
        outcome = self._simulate(self._original_file, self._severity)
        task.return_value(outcome)

    def _simulate(self, file:Gio.File, severity:float):

        original_image = np.asarray(Image.open(file.get_path()).convert('RGB'))

        simulator = simulate.Simulator_AutoSelect()

        protan_array = simulator.simulate_cvd(original_image, simulate.Deficiency.PROTAN, severity=severity)
        deutan_array = simulator.simulate_cvd(original_image, simulate.Deficiency.DEUTAN, severity=severity)
        tritan_array = simulator.simulate_cvd(original_image, simulate.Deficiency.TRITAN, severity=severity)

        protan_im = Image.fromarray(protan_array)
        deutan_im = Image.fromarray(deutan_array)
        tritan_im = Image.fromarray(tritan_array)

        protan_im.save(self._protanopia_file.get_path())
        deutan_im.save(self._deutranopia_file.get_path())
        tritan_im.save(self._tritanopia_file.get_path())

        return self._protanopia_file, self._deutranopia_file, self._tritanopia_file
