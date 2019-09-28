import argparse
import sys
from logging import debug

import zmq

_connect_list = [zmq.REQ, zmq.SUB, zmq.PULL]


def bind_socket(socket_connection: str, socket_type, context=None):
    if socket_type in _connect_list:
        raise ValueError(f'Cannot bind to socket type {socket_type}')
    context = zmq.Context() if context is None else context
    socket = context.socket(socket_type)
    socket.bind(socket_connection)
    debug(f'Bound socket type {socket_type} to {socket_connection}')
    return socket


def connect_socket(socket_connection: str, socket_type, context=None):
    if socket_type not in _connect_list:
        raise ValueError(f'Cannot connect to socket type {socket_type}')
    context = zmq.Context() if context is None else context
    socket = context.socket(socket_type)
    socket.connect(socket_connection)
    debug(f'Connected socket type {socket_type} to {socket_connection}')
    return socket


def subscribe_socket(socket_connection: str, topic=b'', context=None):
    socket = connect_socket(socket_connection, zmq.SUB, context)
    socket.setsockopt(zmq.LINGER, 0)
    socket.setsockopt(zmq.SUBSCRIBE, topic)
    return socket


def create_parser():
    parser = argparse.ArgumentParser(description='Bridge a serial port over zmq pub/sub')
    parser.add_argument('--serial-port', dest='serial_port', type=str,
                        default='', help='Set the serial port (default: /dev/ttyS0 for linux and COM1 for win32)')
    parser.add_argument('--serial-baudrate', dest='serial_baudrate', type=int, default=9600,
                        help='Set the serial baudrate (default: %(default)s)')
    parser.add_argument('--timeout', dest='timeout', type=int, default=1,
                        help='Set the timeout for serial port and zeromq polling (default: %(default)s)')
    parser.add_argument('--streaming-socket', dest='streaming_socket', type=str, default='tcp://*:5555',
                        help='Set the zeromq streaming socket (default: %(default)s)')
    parser.add_argument('--listening-socket', dest='listening_socket', type=str, default='tcp://*:5556',
                        help='Set the zeromq listening port (default: %(default)s)')
    return parser


def parse_pysomq_args(args=None):
    parser = create_parser()
    retrieved_args = parser.parse_args(args)
    if retrieved_args.serial_port == '':
        retrieved_args.serial_port = default_serial_port()
    return retrieved_args


def default_serial_port():
    port = None
    if sys.platform == 'linux' or sys.platform == 'unix':
        port = '/dev/ttyS0'
    elif sys.platform == 'win32':
        port = 'COM1'
    return port
