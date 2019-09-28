import unittest
from logging import debug
from time import sleep

import zmq

from pysomq import SerialServer
from pysomq._utility import subscribe_socket, connect_socket
from tests._utility import listen_socket, listen_feedback_pull, stream_socket, stream_subscribe


class TestSerialServer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSerialServer, self).__init__(*args, **kwargs)
        self._server = None

    def setUp(self) -> None:
        super(TestSerialServer, self).setUp()
        self._server = SerialServer(streaming_socket=stream_socket, listening_socket=listen_socket, timeout=0.001)
        self._server.start()
        while not self._server.is_alive():
            pass
        sleep(0.02)  # Wait until everything is initialized in run -> serial and threads
        debug(f'Server and subscriber setup ann running')

    def tearDown(self) -> None:
        super(TestSerialServer, self).tearDown()
        self._server.terminate()

    def test_streaming(self):
        to_test = 'read\r\n'
        mq_stream_receiver = subscribe_socket(stream_subscribe, topic=b'')
        debug(f'Trying to read from stream')
        received = mq_stream_receiver.recv()
        debug(f'Received from stream: {received}')
        self.assertEqual(to_test, received.decode())

    def test_listening(self):
        to_test = 'sent\r\n'
        mq_feedback = connect_socket(listen_feedback_pull, zmq.PULL)
        mq_config_sender = connect_socket(listen_socket, zmq.REQ)
        debug(f'Send {to_test} over configuration socket')
        mq_config_sender.send(to_test.encode())
        mq_config_sender.recv()
        debug(f'Trying to read from listening')
        received = mq_feedback.recv()
        debug(f'Received from stream: {received}')
        self.assertEqual(to_test, received.decode())

    def test_multi_listening(self):
        to_test1 = 'sent1\r\n'
        to_test2 = 'sent2\r\n'
        mq_feedback = connect_socket(listen_feedback_pull, zmq.PULL)
        mq_config_sender1 = connect_socket(listen_socket, zmq.REQ)
        mq_config_sender2 = connect_socket(listen_socket, zmq.REQ)
        debug(f'Send {to_test1} over configuration socket 1')
        mq_config_sender1.send(to_test1.encode())
        mq_config_sender1.recv()
        debug(f'Trying to read from listening')
        received1 = mq_feedback.recv()
        debug(f'Received from stream: {received1}')
        debug(f'Send {to_test2} over configuration socket 2')
        mq_config_sender2.send(to_test2.encode())
        mq_config_sender2.recv()
        debug(f'Trying to read from listening')
        received2 = mq_feedback.recv()
        debug(f'Received from stream: {received2}')
        self.assertEqual(to_test1, received1.decode())
        self.assertEqual(to_test2, received2.decode())


if __name__ == '__main__':
    unittest.main()
