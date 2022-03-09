from logging import debug
from time import sleep

import zmq
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

from pysomq._utility import bind_socket

from ._utility import listen_feedback_push


class DummySerial:
    def __init__(
        self,
        port=None,
        baudrate=9600,
        bytesize=EIGHTBITS,
        parity=PARITY_NONE,
        stopbits=STOPBITS_ONE,
        timeout=None,
        xonxoff=False,
        rtscts=False,
        write_timeout=None,
        dsrdtr=False,
        inter_byte_timeout=None,
        exclusive=None,
        **kwargs,
    ):
        self._timeout = 0
        self._written = None
        self._line_term = "\r\n"
        self._rate = 0.01
        debug(f"Setup DummySerial write pusher")
        self.line_msg = "read"
        self._mq_feedback = bind_socket(listen_feedback_push, zmq.PUSH)

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def termination(self):
        return self._line_term

    @termination.setter
    def termination(self, value):
        self._line_term = value

    @property
    def rate(self):
        return self._rate

    @property
    def readline_msg(self):
        return f"{self.line_msg}{self.termination}"

    @rate.setter
    def rate(self, value):
        self._rate = value

    def write(self, msg: bytes):
        self._mq_feedback.send(msg)

    def readline(self):
        debug(f"Sleep for {self._rate} seconds")
        sleep(self._rate)
        return self.readline_msg.encode()
