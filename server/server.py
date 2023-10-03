import socketserver
import logging
import json
import tomllib
from datetime import datetime
import argparse
from protocol import *


# Start server.py
class ConnectionHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        '''
        data = self.rfile.readline().strip()
        data = json.loads(data)


        '''


# Args to take:
# Token TTL
# Log level
# Log file location
# Socket file location
# Socket file owners
# Socket file permissions
# Config file location
def parse_args() -> argparse.Namespace:
    pass


# Args to take:
# Token TTL
# Log level
# Log file location
# Socket file location
# Socket file owners
# Socket file permissions
def load_config() -> dict:
    pass


# Merge the arguments from the command line with those read from the configuration file and return the result.
def merge(cmd, conf) -> dict:
    pass


def main() -> None:
    '''
    cmd_args = parse_args()
    conf_args = load_config(cmd_args.conf)
    args = merge(cmd_args, conf_args)

    logger = Logger(args.log_level, args.log_file)
    logger.info("server starting up")

    with socketserver.UnixStreamServer(args.host, ConnectionHandler) as server:
        server_handler = thead.spawn(server.serve_forever())
        running = true
        sig_handler = new signal handler

        while running:
            if sig_handler = SIGTERM:
                server.shutdown()
                logger.log("shutting down")
                running = false

    '''


if __name__ == '__main__':
    main()
