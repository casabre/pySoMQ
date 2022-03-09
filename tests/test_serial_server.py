from logging import debug
from unittest.mock import patch

import zmq

from pysomq._utility import connect_socket, subscribe_socket
from tests._utility import (
    listen_feedback_pull,
    listen_subscribe,
    stream_subscribe,
)


def test_streaming(serial_mock):
    to_test = "read\r\n"
    mq_stream_receiver = subscribe_socket(stream_subscribe, topic=b"")
    debug(f"Trying to read from stream")
    received = mq_stream_receiver.recv()
    debug(f"Received from stream: {received}")
    assert to_test == received.decode()


def test_listening(serial_mock):
    to_test = "sent\r\n"
    mq_feedback = connect_socket(listen_feedback_pull, zmq.PULL)
    mq_config_sender = connect_socket(listen_subscribe, zmq.REQ)
    debug(f"Send {to_test} over configuration socket")
    mq_config_sender.send(to_test.encode())
    mq_config_sender.recv()
    debug(f"Trying to read from listening")
    received = mq_feedback.recv()
    debug(f"Received from stream: {received}")
    assert to_test == received.decode()


def test_multi_listening(serial_mock):
    to_test1 = "sent1\r\n"
    to_test2 = "sent2\r\n"
    mq_feedback = connect_socket(listen_feedback_pull, zmq.PULL)
    mq_config_sender1 = connect_socket(listen_subscribe, zmq.REQ)
    mq_config_sender2 = connect_socket(listen_subscribe, zmq.REQ)
    debug(f"Send {to_test1} over configuration socket 1")
    mq_config_sender1.send(to_test1.encode())
    mq_config_sender1.recv()
    debug(f"Trying to read from listening")
    received1 = mq_feedback.recv()
    debug(f"Received from stream: {received1}")
    debug(f"Send {to_test2} over configuration socket 2")
    mq_config_sender2.send(to_test2.encode())
    mq_config_sender2.recv()
    debug(f"Trying to read from listening")
    received2 = mq_feedback.recv()
    debug(f"Received from stream: {received2}")
    assert to_test1 == received1.decode()
    assert to_test2 == received2.decode()
