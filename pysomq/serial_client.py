import sys
from logging import debug

import zmq

from pysomq._utility import subscribe_socket, connect_socket, parse_pysomq_args


class SerialClient(object):
    def __init__(self, streaming_socket: str = 'tcp://localhost:5555', listening_socket: str = 'tcp://localhost:5556',
                 timeout=1):
        self._mq_context: zmq.context = None
        self._mq_streaming: zmq.socket = None
        self._mq_config: zmq.socket = None
        self._timeout = 0
        self.timeout = timeout
        self._setup_zmq(listening_socket, streaming_socket)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        self._cleanup_zmq()

    def _setup_zmq(self, listening_socket, streaming_socket):
        debug('Setup zmq connections')
        self._mq_context = zmq.Context()
        self._mq_streaming = subscribe_socket(streaming_socket, topic=b'', context=self._mq_context)
        self._mq_streaming.setsockopt(zmq.CONFLATE, True)
        self._mq_streaming.setsockopt(zmq.IMMEDIATE, True)
        self._mq_streaming.sndhwm = 1
        self._mq_config = connect_socket(listening_socket, zmq.REQ, context=self._mq_context)
        self._mq_config.setsockopt(zmq.IMMEDIATE, True)
        self._mq_config.sndhwm = 1

    def _cleanup_zmq(self):
        debug('Cleanup zmq connections')
        self._mq_streaming.unsubscribe('')
        self._mq_streaming.close()
        self._mq_config.close()
        self._mq_context.term()

    @property
    def timeout(self):
        return self._timeout / 1000

    @timeout.setter
    def timeout(self, value):
        self._timeout = value * 1000

    def open(self):
        pass

    def close(self):
        pass

    def readline(self):
        events = self._mq_streaming.poll(timeout=self._timeout)
        if events == zmq.POLLIN:
            return self._mq_streaming.recv()
        else:
            raise TimeoutError

    def write(self, value: bytes):
        self._mq_config.send(value)
        self._mq_config.recv()


if __name__ == '__main__':
    args = parse_pysomq_args(sys.argv[1:])
    client = SerialClient(streaming_socket=args.streaming_socket, listening_socket=args.listening_socket,
                          timeout=args.timeout)
    while True:
        line = client.readline().decode()
        print(line)
