# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import lzma
from gettext import gettext as _
from typing import List

from .compressor import Compressor


class LzmaCompressor(Compressor):
    
    _title = "LZMA"
    _description = _("Compress and decompress using LZMA algorithm")
    _utility_name = "lzma-compressor"

    def compress_text(self, text: str) -> str:
        data = text.encode("utf-8")
        compressed = lzma.compress(data)
        return base64.b64encode(compressed).decode("utf-8")

    def compress_bytes(self, data: bytes) -> str:
        compressed = lzma.compress(data)
        return base64.b64encode(compressed).decode("utf-8")

    def decompress(self, compressed_data: str) -> bytes:
        decoded_data = base64.b64decode(compressed_data.encode())
        return lzma.decompress(decoded_data)

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
            # Check for LZMA magic number (fd 37 7a 58 5a 00)
            return (len(decoded) >= 6 and 
                    decoded[0] == 0xfd and decoded[1] == 0x37 and 
                    decoded[2] == 0x7a and decoded[3] == 0x58 and 
                    decoded[4] == 0x5a and decoded[5] == 0x00)
        except Exception:
            return False
