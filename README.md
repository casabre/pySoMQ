# PySoMQ: Python bindings for serial over ØMQ

This package utilizes the Python bindings of [ØMQ](http://www.zeromq.org) in order to provide a lightweight and fast serial bidirectional [PySerial](https://pypi.org/project/pyserial/) communication interface.

## Getting started

Install the package from Pypi

```bash
pip install pysomq
```

### Run as permanent streaming service

If you want to run the SerialServer as a permanent streamer, please start the module with our specific parameters by

```bash
python -m pysomq --serial-port=YourSerialPort --serial-baudrate=YourBaudrate --timeout=1 --streaming-socket=tcp://*:5555 --listening-socket=tcp://*:5556
```

### Stream from script

If you want to utilize the SerialServer within your own scripts, start streaming by using the following snippet with our parameters

```python
import pysomq


serial_port = '/dev/ttyS0'
baudrate = 9600
stream_socket = 'tcp://*:5555'
listen_socket = 'tcp://*:5556'
timeout = 1
serial_server = pysomq.SerialServer(port='/dev/ttyS0', baudrate=baudrate,
                                    streaming_socket=stream_socket, listening_socket=listen_socket,
                                    timeout=timeout)
serial_server.start()
```

### Receive streaming data

If you want to utilize the SerialServer within your own scripts, start receiving by using the following snippet with our parameters

```python
import pysomq


stream_socket = 'tcp://localhost:5555'
listen_socket = 'tcp://localhost:5556'
timeout = 1

serial_client = pysomq.SerialClient(streaming_socket=stream_socket, listening_socket=listen_socket,
                                    timeout=timeout)
serial_client.write(b'my first line')
answer = serial_client.readline()
```

### Default values

The default values for calling the module or instantiating the classes are

* --serial-port / port: /dev/ttyS0 for Linux and COM1 for Windows

* --serial-baudrate / baudrate: 9600

* --timeout / timeout: 1 second

* --streaming-socket / streaming_socket: tcp://*:5555 respectively tcp://localhost:5555

* --listening-socket / listening_socket: tcp://*:5556 respectively tcp://localhost:5556

## Contributing

I welcome any contributions, enhancements, and bug-fixes.  [Open an issue](https://github.com/casabre/pySoMQ/issues) on GitHub and [submit a pull request](https://github.com/casabre/pySoMQ/pulls).

## License

pySoMQ is 100% free and open-source, under the [MIT license](LICENSE). Use it however you want.

This package is [Treeware](http://treeware.earth). If you use it in production, then we ask that you [**buy the world a tree**](https://plant.treeware.earth/casabre/pySoMQ) to thank us for our work. By contributing to the Treeware forest you’ll be creating employment for local families and restoring wildlife habitats.
