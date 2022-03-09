"""SerialClient class implementation."""
import sys
from logging import debug

import zmq

from ._utility import connect_socket, parse_pysomq_args, subscribe_socket


class SerialClient(object):
    """Receive and send remote serial data."""

    def __init__(
        self,
        streaming_socket: str = "tcp://localhost:5555",
        listening_socket: str = "tcp://localhost:5556",
        timeout=1,
    ):
        """Initialize class."""
        self._mq_context: zmq.context = None
        self._mq_streaming: zmq.socket = None
        self._mq_config: zmq.socket = None
        self._timeout = 0
        self.timeout = timeout
        self._setup_zmq(listening_socket, streaming_socket)

    def __enter__(self):
        """Initialize on enter."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Teardown on exit."""
        pass

    def __del__(self):
        """Cleanup on delete."""
        self._cleanup_zmq()

    def _setup_zmq(self, listening_socket, streaming_socket):
        debug("Setup zmq connections")
        self._mq_context = zmq.Context.instance()
        self._mq_streaming = subscribe_socket(
            streaming_socket, topic=b"", context=self._mq_context
        )
        self._mq_streaming.setsockopt(
            zmq.CONFLATE, True  # pylint: disable=E1101
        )
        self._mq_streaming.setsockopt(
            zmq.IMMEDIATE, True  # pylint: disable=E1101
        )
        self._mq_streaming.sndhwm = 1
        self._mq_config = connect_socket(
            listening_socket,
            zmq.REQ,  # pylint: disable=E1101
            context=self._mq_context,
        )
        self._mq_config.setsockopt(
            zmq.IMMEDIATE, True  # pylint: disable=E1101
        )
        self._mq_config.sndhwm = 1

    def _cleanup_zmq(self):
        debug("Cleanup zmq connections")
        if self._mq_streaming:
            self._mq_streaming.unsubscribe("")
            self._mq_streaming.close()
        if self._mq_config:
            self._mq_config.close()

    @property
    def timeout(self):
        """Get timeout for zmq polling."""
        return self._timeout / 1000

    @timeout.setter
    def timeout(self, value):
        """Set timeout for zmq polling."""
        self._timeout = value * 1000

    def readline(self):
        """Read a streamed line."""
        events = self._mq_streaming.poll(timeout=self._timeout)
        if events == zmq.POLLIN:
            return self._mq_streaming.recv()
        else:
            raise TimeoutError

    def write(self, value: bytes):
        """Write to remote serial connection."""
        self._mq_config.send(value)
        self._mq_config.recv()
