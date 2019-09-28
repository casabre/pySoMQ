import unittest
from logging import debug
from time import sleep

import zmq

from pysomq import SerialServer, SerialClient
from pysomq._utility import connect_socket
from tests._utility import listen_socket, listen_feedback_pull, stream_socket


class TestSerialClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSerialClient, self).__init__(*args, **kwargs)
        self._server = None

    def setUp(self) -> None:
        super(TestSerialClient, self).setUp()
        self._server = SerialServer(stream_socket, listen_socket, timeout=0.001)
        self._server.start()
        while not self._server.is_alive():
            pass
        self._client = SerialClient(streaming_socket=stream_socket, listening_socket=listen_socket)
        sleep(0.02)  # Wait until everything is initialized in run -> serial and threads
        debug(f'Server and client setup ann running')

    def tearDown(self) -> None:
        super(TestSerialClient, self).tearDown()
        self._server.terminate()

    def test_streaming(self):
        to_test = 'read\r\n'
        debug(f'Trying to read from client')
        received = self._client.readline()
        debug(f'Received from client: {received}')
        self.assertEqual(to_test, received.decode())

    def test_listening(self):
        to_test = 'sent\r\n'
        mq_feedback = connect_socket(listen_feedback_pull, zmq.PULL)
        debug(f'Send {to_test} over client')
        self._client.write(to_test.encode())
        debug(f'Trying to read from feedback socket')
        received = mq_feedback.recv()
        debug(f'Received from feedback socket: {received}')
        self.assertEqual(to_test, received.decode())


if __name__ == '__main__':
    unittest.main()
