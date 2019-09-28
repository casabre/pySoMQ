from pysomq.serial_client import SerialClient
from pysomq.serial_server import SerialServer

__all__ = ['__version__', 'SerialServer', 'SerialClient']

try:
    from ._version import version as __version__
except ImportError:
    # broken installation, we don't even try
    # unknown only works because I do poor mans version compare
    __version__ = "unknown"
