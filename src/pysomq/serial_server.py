"""SerialServer class implementation."""
import typing
from logging import debug
from threading import Thread

import zmq
from serial import Serial

from ._utility import bind_socket, default_serial_port


class SerialServer(object):
    """Stream and receive remote serial data."""

    def __init__(
        self,
        streaming_socket: str = "tcp://*:5555",
        listening_socket: str = "tcp://*:5556",
        timeout=1,
        *args,
        **kwargs,
    ):
        """Initialize class."""
        self._run = False
        self._mq_context = None
        self._mq_streaming = None
        self._mq_listening = None
        self._streaming_socket = streaming_socket
        self._listening_socket = listening_socket
        self._serial_port = default_serial_port()
        self._baudrate = 9600
        if "port" in kwargs:
            self._serial_port = kwargs.pop("port")
        if "baudrate" in kwargs:
            self._baudrate = kwargs.pop("baudrate")
        self._serial: typing.Optional[Serial] = None
        self.timeout = timeout  # [s]
        super(SerialServer, self).__init__(*args, **kwargs)

    def __enter__(self):
        """Initialize on enter."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Teardown on exit."""
        self._run = False

    def __del__(self):
        """Cleanup on delete."""
        self._run = False

    @property
    def timeout(self):
        """Get timeout for zeroMQ polling and serial port.

        :return: timeout value in seconds
        """
        return self._timeout / 1000

    @timeout.setter
    def timeout(self, value):
        """Set timeout for zeroMQ polling and serial port.

        :param value: timeout value in seconds
        :return: None
        """
        self._timeout = value * 1000
        if self._serial is not None:
            self._serial.timeout(value / 1000)

    @property
    def running(self) -> bool:
        """Server is running."""
        return self._run

    def start(self) -> None:
        """Start the server."""
        self._run = True
        self._setup_zmq()
        self._setup_serial()
        self._run_threads()

    def stop(self) -> None:
        """Stop the server."""
        self._run = False
        self.join()
        self._cleanup_zmq()

    def join(self):
        """Wait until sub-threads are finished."""
        debug("Join threads")
        for thread in self._threads:
            thread.join()

    def _run_threads(self):
        debug("Setup threads")
        self._threads = [
            Thread(target=self._run_read_and_stream),
            Thread(target=self._run_listen_and_write),
        ]
        debug("Start threads")
        for thread in self._threads:
            thread.start()

    def _setup_serial(self):
        debug("Setup serial connection")
        self._serial = Serial(
            port=self._serial_port,
            baudrate=self._baudrate,
            timeout=self.timeout,
        )

    def _setup_zmq(self):
        debug("Setup zmq connections")
        self._mq_context = zmq.Context.instance()
        self._mq_streaming = bind_socket(
            self._streaming_socket,
            zmq.PUB,  # pylint: disable=E1101
            self._mq_context,
        )
        self._mq_streaming.setsockopt(
            zmq.CONFLATE, True  # pylint: disable=E1101
        )
        self._mq_streaming.setsockopt(
            zmq.IMMEDIATE, True  # pylint: disable=E1101
        )
        self._mq_listening = bind_socket(
            self._listening_socket,
            zmq.REP,  # pylint: disable=E1101
            self._mq_context,
        )
        self._mq_listening.setsockopt(
            zmq.IMMEDIATE, True  # pylint: disable=E1101
        )

    def _cleanup_zmq(self):
        debug("Cleanup zmq connections")
        if self._mq_streaming:
            self._mq_streaming.close()
        if self._mq_listening:
            self._mq_listening.close()

    def _run_read_and_stream(self):
        debug(f"Starting streaming")
        while self._run:
            try:
                line = typing.cast(Serial, self._serial).readline()
                debug(f"Received from serial: {line}")
                typing.cast(zmq.Socket, self._mq_streaming).send(line)
            except Exception as e:
                self._run = False
                raise e

    def _run_listen_and_write(self):
        poller = zmq.Poller()
        poller.register(self._mq_listening, zmq.POLLIN)
        debug(
            f"Start polling at write connection "
            f"with timeout {self._timeout} ms"
        )
        while self._run:
            try:
                socks = dict(poller.poll(timeout=self._timeout))
                if (
                    self._mq_listening in socks
                    and socks[self._mq_listening] == zmq.POLLIN
                ):
                    msg = typing.cast(zmq.Socket, self._mq_listening).recv()
                    typing.cast(zmq.Socket, self._mq_listening).send(b"")
                    debug(f"Received from zmq: {msg}")
                    typing.cast(Serial, self._serial).write(msg)
            except Exception as e:
                self._run = False
                raise e
