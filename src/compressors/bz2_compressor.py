# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import bz2
from gettext import gettext as _
from typing import List

from .compressor import Compressor


class Bz2Compressor(Compressor):
    
    _title = "Bzip2"
    _description = _("Compress and decompress using Bzip2 algorithm")
    _utility_name = "bz2-compressor"

    def compress_text(self, text: str) -> str:
        data = text.encode("utf-8")
        compressed = bz2.compress(data)
        return base64.b64encode(compressed).decode("utf-8")

    def compress_bytes(self, data: bytes) -> str:
        compressed = bz2.compress(data)
        return base64.b64encode(compressed).decode("utf-8")

    def decompress(self, compressed_data: str) -> bytes:
        decoded_data = base64.b64decode(compressed_data.encode())
        return bz2.decompress(decoded_data)

    def get_title(self) -> str:
        return self._title

    def get_description(self) -> str:
        return self._description

    def get_utility_name(self) -> str:
        return self._utility_name

    def get_file_extensions(self) -> List[str]:
        return self._extensions

    def can_decompress(self, data: str) -> bool:
        try:
            decoded = base64.b64decode(data.encode())
            # Check for Bzip2 magic number (42 5a)
            return len(decoded) >= 2 and decoded[0] == 0x42 and decoded[1] == 0x5a
        except Exception:
            return False
