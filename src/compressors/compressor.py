# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List


class Compressor(ABC):
    """Base class for all compressors"""

    @abstractmethod
    def compress_text(self, text: str) -> str:
        """Compress text and return base64 encoded result"""
        pass

    @abstractmethod
    def compress_bytes(self, data: bytes) -> str:
        """Compress bytes and return base64 encoded result"""
        pass

    @abstractmethod
    def decompress(self, compressed_data: str) -> bytes:
        """Decompress base64 encoded data and return bytes"""
        pass

    @abstractmethod
    def get_title(self) -> str:
        """Get the compressor title"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get the compressor description"""
        pass

    @abstractmethod
    def get_utility_name(self) -> str:
        """Get unique utility name for this compressor"""
        pass

    @abstractmethod
    def can_decompress(self, data: str) -> bool:
        """Check if this compressor can decompress the given data"""
        pass
