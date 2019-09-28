from logging import basicConfig, DEBUG
from sys import platform

basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if platform == 'linux':
    stream_socket = 'ipc:///tmp/stream'
    listen_socket = 'ipc:///tmp/listen'
    stream_subscribe = stream_socket
    listen_feedback_push = 'ipc:///tmp/feedback'
    listen_feedback_pull = listen_feedback_push
else:
    stream_socket = 'tcp://*:5555'
    listen_socket = 'tcp://*:5556'
    stream_subscribe = 'tcp://localhost:5555'
    listen_feedback_push = 'tcp://*:5557'
    listen_feedback_pull = 'tcp://localhost:5557'
