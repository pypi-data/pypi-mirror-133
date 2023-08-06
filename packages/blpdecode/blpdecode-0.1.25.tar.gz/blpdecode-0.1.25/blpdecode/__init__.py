"""Top-level package for blpdecode."""

from .blpdecode import decode
from .cli import cli

__all__ = ["cli", "decode"]

__author__ = "Matt Krueger"
__email__ = "mkrueger@rstms.net"
__version__ = "0.1.25"
