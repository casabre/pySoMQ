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
