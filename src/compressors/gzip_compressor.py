# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import gzip
from io import BytesIO
from gettext import gettext as _
from typing import List

from .compressor import Compressor


class GzipCompressor(Compressor):

    _title = "GZip"
    _description = _("Compress and decompress using GZip algorithm")
    _utility_name = "gzip-compressor"

    def compress_text(self, text: str) -> str:
        data = text.encode("utf-8")
        compressed = gzip.compress(data)
        return base64.b64encode(compressed).decode("utf-8")

    def compress_bytes(self, data: bytes) -> str:
        with BytesIO() as buffer:
            with gzip.GzipFile(fileobj=buffer, mode='wb') as comp_file:
                comp_file.write(data)
            compressed_data = buffer.getvalue()
        return base64.b64encode(compressed_data).decode("utf-8")

    def decompress(self, compressed_data: str) -> bytes:
        decoded_data = base64.b64decode(compressed_data.encode())
        with gzip.open(BytesIO(decoded_data), 'rb') as comp_file:
            return comp_file.read()

    def get_title(self) -> str:
        return self._title

    def get_description(self) -> str:
        return self._description

    def get_utility_name(self) -> str:
        return self._utility_name

    def can_decompress(self, data: str) -> bool:
        try:
            decoded = base64.b64decode(data.encode())
            # Check for GZip magic number (1f 8b)
            return len(decoded) >= 2 and decoded[0] == 0x1f and decoded[1] == 0x8b
        except Exception:
            return False
