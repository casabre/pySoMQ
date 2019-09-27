import argparse
import sys

from .serial_client import SerialClient
from .serial_server import SerialServer

__all__ = ['__version__', 'main', 'SerialServer', 'SerialClient']

try:
    from ._version import version as __version__
except ImportError:
    # broken installation, we don't even try
    # unknown only works because I do poor mans version compare
    __version__ = "unknown"


def main(args=None):
    parser = argparse.ArgumentParser(description='Bridge a serial port over zmq pub/sub')
    parser.add_argument('--serial-port', dest='serial_port', type=str,
                        default='', help='Set the serial port (default: %(default)s)')
    parser.add_argument('--serial-baudrate', dest='baudrate', type=int, default=9600,
                        help='Set the serial baudrate (default: %(default)s)')
    parser.add_argument('--timeout', dest='timeout', type=int, default=1,
                        help='Set the timeout for serial port and zeromq polling (default: %(default)s)')
    parser.add_argument('--streaming-socket', dest='streaming_socket', type=str, default='tcp://*:5555',
                        help='Set the zeromq streaming socket (default: %(default)s)')
    parser.add_argument('--listening-socket', dest='listening_socket', type=int, default='tcp://*:5556',
                        help='Set the zeromq listening port (default: %(default)s)')
    args = parser.parse_args(args)
    server = SerialServer(streaming=args.streaming_socket, listening=args.listening_socket, port=args.serial_port,
                          baudrate=args.baudrate)
    server.timeout = args.timeout
    server.daemon = True
    server.name = 'SerialServer'
    server.start()
    print(f'Started SerialServer daemon with the following configuration:\n'
          f'Serial configuration: Port {args.serial_port}, Baudrate {args.baudrate}, Timeout {args.timeout}\n'
          f'Streaming configuration: Socket "{args.streaming_socket}"\n'
          f'Listening configuration: Socket "{args.listening_socket}"')


if __name__ == '__main__':
    main(sys.argv[:-1])