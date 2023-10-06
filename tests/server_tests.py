import unittest
import argparse
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch  # Use unittest.mock.patch
from server import parse_args

import unittest
from server import Config, LogLevel


class TestServer(unittest.TestCase):

    def test_initial_values(self):
        config = Config()
        self.assertEqual(config.ttl, 60)
        self.assertIsNone(config.log)
        self.assertEqual(config.log_level, LogLevel.INFO)
        self.assertEqual(config.socket, Path("/run/pw_rest.socket"))
        self.assertEqual(config.socket_perm, 0o0600)
        self.assertIsNone(config.socket_owners)

    def test_set_attributes(self):
        config = Config()
        config.build({
            'ttl': 90,
            'log': Path('/var/log/pw_reset.log'),
            'log_level': LogLevel.DEBUG,
            'socket': Path('/custom/socket'),
            'socket_perm': 0o0644,
            'socket_owners': ('user', 'group')
        })

        self.assertEqual(config.ttl, 90)
        self.assertEqual(config.log, Path('/var/log/pw_reset.log'))
        self.assertEqual(config.log_level, LogLevel.DEBUG)
        self.assertEqual(config.socket, Path('/custom/socket'))
        self.assertEqual(config.socket_perm, 0o0644)
        self.assertEqual(config.socket_owners, ('user', 'group'))

    def test_iteration(self):
        config = Config()
        config.build({
            'ttl': 90,
            'log': Path('/var/log/pw_reset.log'),
            'socket_perm': 0o0644
        })

        # Test iteration and conversion to dictionary
        config_dict = dict(config)
        expected_dict = {
            'ttl': 90,
            'log': Path('/var/log/pw_reset.log'),
            'log_level': LogLevel.INFO,
            'socket': Path('/run/pw_rest.socket'),
            'socket_perm': 0o0644,
            'socket_owners': None
        }
        self.assertEqual(config_dict, expected_dict)

    def test_unknown_parameter(self):
        config = Config()
        with self.assertRaises(TypeError):
            config.build({'unknown_param': 'value'})


if __name__ == '__main__':
    unittest.main()
