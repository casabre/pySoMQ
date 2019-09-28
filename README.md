# PySoMQ: Python bindings for serial over ØMQ

This package utilizes the Python bindings of [ØMQ](http://www.zeromq.org) 
in order to provide a lightweight and fast serial bidirectional 
[PySerial](https://pypi.org/project/pyserial/) communication interface.

## Getting started
### Run as permanent streaming service
If you want to run the SerialServer as a permanent streamer, please 
start the module with our specific parameters by
```bash
$ python -m pysomq --serial-port=YourSerialPort --serial-baudrate=YourBaudrate --timeout=1 --streaming-socket=tcp://*:5555 --listening-socket=tcp://*:5556
```

### Stream from script
If you want to utilize the SerialServer within your own scripts, start
streaming by using the following snippet with our parameters
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
If you want to utilize the SerialServer within your own scripts, start 
receiving by using the following snippet with our parameters
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

## Development

You can get the latest source code from my 
[Gitlab](https://gitlab.com/casabre/pysomq)
 repository. For extension or bugfixes, please create a new branch with
  final merge request. Any contribution is appreciated!
  
Currently, the Linux and Windows versions are tested and verified. OSX
and cygwin support has to be tested.