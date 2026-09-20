"""Пакет с классами предметной области."""

from .conferences import Conference
from .sections import Section
from .talks import Talk

__all__ = ["Conference", "Section", "Talk"]
