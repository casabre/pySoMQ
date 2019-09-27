import zmq

from ._utility import subscribe_socket, connect_socket


class SerialClient(object):
    def __init__(self, streaming_socket: str = 'tcp://localhost:5555', config_socket: str = 'tcp://localhost:5556',
                 timeout=1):
        self._mq_context = None
        self._mq_streaming = None
        self._mq_config = None
        self._timeout = 0
        self.timeout = timeout
        self._setup_zmq(config_socket, streaming_socket)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup_zmq()

    def __del__(self):
        self._cleanup_zmq()

    def _setup_zmq(self, config_socket, streaming_socket):
        self._mq_context = zmq.Context()
        self._mq_streaming = subscribe_socket(streaming_socket, topic=b'', context=self._mq_context)
        self._mq_streaming.setsockopt(zmq.CONFLATE, True)
        self._mq_streaming.setsockopt(zmq.IMMEDIATE, True)
        self._mq_config = connect_socket(config_socket, zmq.REQ, context=self._mq_context)
        self._mq_config.setsockopt(zmq.IMMEDIATE, True)

    def _cleanup_zmq(self):
        self._mq_streaming.unsubscribe()
        self._mq_config.unsubscribe()
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
