# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import zlib
from gi.repository import Gio, GObject
import hashlib
import io


class HashGeneratorService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_input(self, input_text_or_file_path:str):
        self._input = input_text_or_file_path

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._input = None
        return result.propagate_value().value

    def hash_text_with_md5_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_md5_thread)

    def _hash_text_with_md5_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_md5(self._input)
        task.return_value(outcome)

    def _hash_text_with_md5(self, text:str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def hash_file_with_md5_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_md5_thread)

    def _hash_file_with_md5_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_md5(self._input)
        task.return_value(outcome)

    def _hash_file_with_md5(self, file_path:str):
        md5 = hashlib.md5()
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def hash_text_with_sha1_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_sha1_thread)

    def _hash_text_with_sha1_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_sha1(self._input)
        task.return_value(outcome)

    def _hash_text_with_sha1(self, text:str):
        return hashlib.sha1(text.encode("utf-8")).hexdigest()

    def hash_file_with_sha1_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_sha1_thread)

    def _hash_file_with_sha1_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_sha1(self._input)
        task.return_value(outcome)

    def _hash_file_with_sha1(self, file_path:str):
        sha1 = hashlib.sha1()
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                sha1.update(chunk)
        return sha1.hexdigest()

    def hash_text_with_sha256_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_sha256_thread)

    def _hash_text_with_sha256_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_sha256(self._input)
        task.return_value(outcome)

    def _hash_text_with_sha256(self, text:str):
         return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def hash_file_with_sha256_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_sha256_thread)

    def _hash_file_with_sha256_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_sha256(self._input)
        task.return_value(outcome)

    def _hash_file_with_sha256(self, file_path:str):
        sha256 = hashlib.sha256()
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def hash_text_with_sha512_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_sha512_thread)

    def _hash_text_with_sha512_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_sha512(self._input)
        task.return_value(outcome)

    def _hash_text_with_sha512(self, text:str):
         return hashlib.sha512(text.encode("utf-8")).hexdigest()

    def hash_file_with_sha512_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_sha512_thread)

    def _hash_file_with_sha512_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_sha512(self._input)
        task.return_value(outcome)

    def _hash_file_with_sha512(self, file_path:str):
        sha512 = hashlib.sha512()
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                sha512.update(chunk)
        return sha512.hexdigest()

    def hash_text_with_sha3_256_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_sha3_256_thread)

    def _hash_text_with_sha3_256_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_sha3_256(self._input)
        task.return_value(outcome)

    def _hash_text_with_sha3_256(self, text:str):
        return hashlib.sha3_256(text.encode("utf-8")).hexdigest()

    def hash_file_with_sha3_256_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_sha3_256_thread)

    def _hash_file_with_sha3_256_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_sha3_256(self._input)
        task.return_value(outcome)

    def _hash_file_with_sha3_256(self, file_path:str):
        sha3_256 = hashlib.sha3_256()
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                sha3_256.update(chunk)
        return sha3_256.hexdigest()

    def hash_text_with_sha3_512_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_sha3_512_thread)

    def _hash_text_with_sha3_512_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_sha3_512(self._input)
        task.return_value(outcome)

    def _hash_text_with_sha3_512(self, text:str):
        return hashlib.sha3_512(text.encode("utf-8")).hexdigest()

    def hash_file_with_sha3_512_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_sha3_512_thread)

    def _hash_file_with_sha3_512_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_sha3_512(self._input)
        task.return_value(outcome)

    def _hash_file_with_sha3_512(self, file_path:str):
        sha3_512 = hashlib.sha3_512()
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                sha3_512.update(chunk)
        return sha3_512.hexdigest()

    def hash_text_with_adler32_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_adler32_thread)

    def _hash_text_with_adler32_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_adler32(self._input)
        task.return_value(outcome)

    def _hash_text_with_adler32(self, text:str):
        return format(zlib.adler32(text.encode("utf-8")), '08x')

    def hash_file_with_adler32_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_adler32_thread)

    def _hash_file_with_adler32_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_adler32(self._input)
        task.return_value(outcome)

    def _hash_file_with_adler32(self, file_path:str):
        adler32 = 1
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                adler32 = zlib.adler32(chunk, adler32)
        return format(adler32, '08x')

    def hash_text_with_crc32_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_text_with_crc32_thread)

    def _hash_text_with_crc32_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_text_with_crc32(self._input)
        task.return_value(outcome)

    def _hash_text_with_crc32(self, text:str):
        return format(zlib.crc32(text.encode("utf-8")), '08x')

    def hash_file_with_crc32_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._hash_file_with_crc32_thread)

    def _hash_file_with_crc32_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._hash_file_with_crc32(self._input)
        task.return_value(outcome)

    def _hash_file_with_crc32(self, file_path:str):
        crc32 = 0
        with io.open(file_path, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b''):
                crc32 = zlib.crc32(chunk, crc32)
        return format(crc32, '08x')