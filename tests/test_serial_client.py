from logging import debug
from time import sleep

import pytest
import zmq

from pysomq import SerialClient
from pysomq._utility import connect_socket
from tests._utility import (
    listen_feedback_pull,
    listen_subscribe,
    stream_subscribe,
)


@pytest.fixture
def serial_client() -> SerialClient:
    client = SerialClient(
        streaming_socket=stream_subscribe,
        listening_socket=listen_subscribe,
    )
    sleep(
        0.02
    )  # Wait until everything is initialized in run -> serial and threads
    debug(f"Server and client setup ann running")
    yield client


def test_streaming(serial_mock, serial_client):
    to_test = "read\r\n"
    debug(f"Trying to read from client")
    received = serial_client.readline()
    debug(f"Received from client: {received}")
    assert to_test == received.decode()


def test_listening(serial_mock, serial_client):
    to_test = "sent\r\n"
    mq_feedback = connect_socket(listen_feedback_pull, zmq.PULL)
    debug(f"Send {to_test} over client")
    serial_client.write(to_test.encode())
    debug(f"Trying to read from feedback socket")
    received = mq_feedback.recv()
    debug(f"Received from feedback socket: {received}")
    assert to_test == received.decode()
