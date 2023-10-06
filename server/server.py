import socketserver
import logging
import json
import tomllib
from datetime import datetime
import argparse
from protocol import *


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Config:
    def __init__(self):
        self._ttl: int = 60  # Time to live in number of minutes
        self._log: Path | None = None
        self._log_level: LogLevel = LogLevel.INFO
        self._socket: Path = Path("/run/pw_rest.socket")
        self._socket_perm: int = 0o0600  # Unix mode in octol.
        self._socket_owners: tuple[str, str] | None = None

        # List of attribute names for iteration
        self._attributes = [
            'ttl',
            'log',
            'log_level',
            'socket',
            'socket_perm',
            'socket_owners'
        ]

    @property
    def ttl(self) -> int:
        return self._ttl

    @property
    def log(self) -> Path:
        return self._log

    @property
    def log_level(self) -> LogLevel:
        return self._log_level

    @property
    def socket(self) -> Path:
        return self._socket

    @property
    def socket_perm(self) -> int:
        return self._socket_perm

    @property
    def socket_owners(self) -> tuple[str, str]:
        return self._socket_owners

    def build(self, arguments: dict[str, int | Path | tuple[str, str] | None]) -> None:
        for key, value in arguments.items():
            if value is not None:
                match key:
                    case 'ttl':
                        self._ttl = value
                    case 'log':
                        self._log = value
                    case 'log_level':
                        self._log_level = value
                    case 'socket':
                        self._socket = value
                    case 'socket_perm':
                        self._socket_perm = value
                    case 'socket_owners':
                        self._socket_owners = value
                    case _:
                        raise TypeError("Unknown parameter: {}".format(key))

    def __iter__(self):
        self._attributes_iterated = set()
        return self

    def __next__(self):
        # Define how the class should be iterated to yield key-value pairs
        for attr_name in self._attributes:
            if attr_name not in self._attributes_iterated:
                self._attributes_iterated.add(attr_name)
                return attr_name, getattr(self, attr_name)
        # Raise StopIteration when there are no more attributes to yield
        raise StopIteration


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
