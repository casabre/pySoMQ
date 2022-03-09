import os
from time import sleep
from unittest.mock import patch

import pytest

from pysomq import SerialServer
from tests._utility import listen_socket, stream_socket

from .DummySerial import DummySerial

if os.name == "nt":  # sys.platform == 'win32':
    where = "serial.serialwin32.Serial"
elif os.name == "posix":
    where = "serial.serialposix.Serial"
elif os.name == "java":
    where = "serial.serialjava.Serial"


@pytest.fixture
def serial_mock() -> SerialServer:
    with patch(target="pysomq.serial_server.Serial", new=DummySerial) as p:
        server = SerialServer(
            streaming_socket=stream_socket,
            listening_socket=listen_socket,
            timeout=0.001,
        )
        server.start()
        sleep(
            0.02
        )  # Wait until everything is initialized in run -> serial and threads
        yield p
        server.stop()
