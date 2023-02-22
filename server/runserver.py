import sys
from wsgiref.simple_server import make_server

import config.urls
from server.handler import app


def run(host, port):
    try:
        server = make_server(host, port, app)
        print(
            f'The server is running on http://{host}:{port}/\n'
            'Quit the server with CONTROL-C.'
        )
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...')
        server.server_close()


def initialize():
    host = '127.0.0.1'

    try:
        if len(sys.argv) > 2:
            port = int(sys.argv[2])
            run(host, port)
        else:
            port = 8000
            run(host, port)
    except (OSError, ValueError):
        print(f'The port is not available.')
