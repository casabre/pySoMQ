"""Python serial over zmq."""
import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version
else:
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass


from .serial_client import SerialClient
from .serial_server import SerialServer

__all__ = ["__version__", "SerialServer", "SerialClient"]
