"""Decode Barracuda email filter's LinkProtect encoded URLs"""

from .blpdecode import decode
from .cli import cli
from .version import __version__

__all__ = ["cli", "decode", "__version__"]
