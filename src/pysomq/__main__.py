"""pysomq module call."""
import os
import sys

from ._utility import parse_pysomq_args
from .serial_server import SerialServer


def main(args=None):
    """Run server."""
    args = parse_pysomq_args(args)
    server = SerialServer(
        streaming_socket=args.streaming_socket,
        listening_socket=args.listening_socket,
        port=args.serial_port,
        baudrate=args.serial_baudrate,
    )
    server.timeout = args.timeout
    server.start()
    print(
        f"Started SerialServer daemon with the following configuration:\n"
        f"Module process id: {os.getpid()}\n"
        f"Serial configuration: Port {args.serial_port}, "
        f"Baudrate {args.serial_baudrate}, Timeout {args.timeout}\n"
        f'Streaming configuration: Socket "{args.streaming_socket}"\n'
        f'Listening configuration: Socket "{args.listening_socket}"'
    )
    server.join()


if __name__ == "__main__":
    main(sys.argv[1:])
