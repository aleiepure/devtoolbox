# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from lxml import etree


class XmlValidatorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_xml(self, xml:str):
        self._xml = xml

    def set_xsd(self, xsd:str):
        self._xsd = xsd

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._xml = None
        self._xsd = None
        return result.propagate_value().value

    def check_xml_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._check_xml_thread)

    def _check_xml_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._check_xml(self._xml, self._xsd)
        task.return_value(outcome)

    def _check_xml(self, xml:str, xsd:str):

        parser = etree.XMLParser(no_network=False)

        try:
            schema_root = etree.fromstring(bytes(xsd, encoding="utf-8"), parser=parser)
            schema = etree.XMLSchema(etree=schema_root)
            try:
                schema.assertValid(etree.fromstring(bytes(xml, encoding='utf-8'), parser=parser))
                return True, None, None
            except etree.DocumentInvalid as error:
                return False, error, None
        except etree.XMLSchemaParseError as error:
            return False, None, error
