import argparse
import sys
from unittest.mock import patch

from pysomq._utility import parse_pysomq_args

if sys.platform == "linux":
    port = "/dev/ttyS0"
elif sys.platform == "win32":
    port = "COM1"
baudrate = 9600
timeout = 1
streaming_socket = "tcp://*:5555"
listening_socket = "tcp://*:5556"


def test_defaults():
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            serial_port=port,
            serial_baudrate=baudrate,
            timeout=timeout,
            streaming_socket=streaming_socket,
            listening_socket=listening_socket,
        ),
    ) as m:
        args = parse_pysomq_args()
        assert args.serial_port == port
        assert args.serial_baudrate == baudrate
        assert args.timeout == timeout
        assert args.streaming_socket == streaming_socket
        assert args.listening_socket == listening_socket
