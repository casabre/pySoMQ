import os
from logging import debug
from multiprocessing import Process
from threading import Thread

import zmq

from pysomq._utility import bind_socket, default_serial_port

if not os.environ.get('UNITTEST'):
    from serial import Serial
else:
    from tests.DummySerial import DummySerial as Serial


class SerialServer(Process):
    def __init__(self, streaming_socket: str = 'tcp://*:5555', listening_socket: str = 'tcp://*:5556', timeout=1,
                 *args, **kwargs):
        self._run = False
        self._mq_context = None
        self._mq_streaming = None
        self._mq_listening = None
        self._streaming_socket = streaming_socket
        self._listening_socket = listening_socket
        self._serial_port = default_serial_port()
        self._baudrate = 9600
        if 'port' in kwargs:
            self._serial_port = kwargs.pop('port')
        if 'baudrate' in kwargs:
            self._baudrate = kwargs.pop('baudrate')
        self._serial: Serial = None
        self.timeout = timeout  # [s]
        super(SerialServer, self).__init__(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._run = False

    def __del__(self):
        self._run = False

    @property
    def timeout(self):
        """
        Get timeout for zeroMQ polling and serial port
        :return: timeout value in seconds
        """
        return self._timeout / 1000

    @timeout.setter
    def timeout(self, value):
        """
        Set timeout for zeroMQ polling and serial port
        :param value: timeout value in seconds
        :return: None
        """
        self._timeout = value * 1000
        if self._serial is not None:
            self._serial.timeout(value / 1000)

    def start(self) -> None:
        self._run = True
        super(SerialServer, self).start()

    def stop(self) -> None:
        self._run = False

    def terminate(self) -> None:
        self._run = False
        super(SerialServer, self).terminate()

    def run(self) -> None:
        self._setup_zmq()
        self._setup_serial()
        self._run_threads()
        self._cleanup_zmq()

    def _run_threads(self):
        debug('Setup threads')
        threads = [Thread(target=self._run_read_and_stream), Thread(target=self._run_listen_and_write)]
        debug('Start threads')
        for thread in threads:
            thread.start()
        debug('Join threads')
        for thread in threads:
            thread.join()

    def _setup_serial(self):
        debug('Setup serial connection')
        self._serial: Serial = Serial(port=self._serial_port, baudrate=self._baudrate, timeout=self.timeout)

    def _setup_zmq(self):
        debug('Setup zmq connections')
        self._mq_context = zmq.Context()
        self._mq_streaming = bind_socket(self._streaming_socket, zmq.PUB, self._mq_context)
        self._mq_streaming.setsockopt(zmq.CONFLATE, True)
        self._mq_streaming.setsockopt(zmq.IMMEDIATE, True)
        self._mq_listening = bind_socket(self._listening_socket, zmq.REP, self._mq_context)
        self._mq_listening.setsockopt(zmq.IMMEDIATE, True)

    def _cleanup_zmq(self):
        debug('Cleanup zmq connections')
        self._mq_streaming.close()
        self._mq_listening.close()
        self._mq_context.term()

    def _run_read_and_stream(self):
        debug(f'Starting streaming')
        while self._run:
            try:
                line = self._serial.readline()
                debug(f'Received from serial: {line}')
                self._mq_streaming.send(line)
            except Exception as e:
                self._run = False
                raise e

    def _run_listen_and_write(self):
        poller = zmq.Poller()
        poller.register(self._mq_listening, zmq.POLLIN)
        debug(f'Start polling at write connection with timeout {self._timeout} ms')
        while self._run:
            try:
                socks = dict(poller.poll(timeout=self._timeout))
                if self._mq_listening in socks and socks[self._mq_listening] == zmq.POLLIN:
                    msg = self._mq_listening.recv()
                    self._mq_listening.send(b'')
                    debug(f'Received from zmq: {msg}')
                    self._serial.write(msg)
            except Exception as e:
                self._run = False
                raise e
