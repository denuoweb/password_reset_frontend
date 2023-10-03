import unittest
from datetime import datetime
from protocol import Request, Response, Lookup, Update, Token, Success, Error, message_builder


class TestMessageProtocol(unittest.TestCase):
    def test_request_serialization(self):
        request = Request('john_doe', 'password123')
        expected_json = '{"message_type": "Request", "username": "john_doe", "password": "password123"}'
        self.assertEqual(str(request), expected_json)

    def test_response_serialization(self):
        response = Response(username='john_doe', foo='foo', bar='bar')
        expected_json = '{"message_type": "Response", "username": "john_doe", "foo": "foo", "bar": "bar"}'
        self.assertEqual(str(response), expected_json)

    def test_lookup_request_creation(self):
        lookup_request = Lookup('john_doe')
        self.assertEqual(lookup_request.username, 'john_doe')

    def test_update_request_creation(self):
        update_request = Update('jane_doe', 'new_password')
        self.assertEqual(update_request.username, 'jane_doe')
        self.assertEqual(update_request.password, 'new_password')

    def test_token_response_creation(self):
        now = datetime.now()
        token_response = Token('john_doe', now)
        self.assertEqual(token_response.username, 'john_doe')
        self.assertEqual(token_response.creation_time, now)

    def test_success_response_creation(self):
        success_response = Success()
        self.assertEqual(success_response.message_type, 'Success')

    def test_error_response_creation(self):
        error_response = Error('Invalid username')
        self.assertEqual(error_response.error, 'Invalid username')

    def test_message_builder(self):
        json_str = '{"message_type": "Update", "username": "jane_doe", "password": "new_password"}'
        message = message_builder(json_str)
        self.assertIsInstance(message, Update)
        self.assertEqual(message.username, 'jane_doe')
        self.assertEqual(message.password, 'new_password')


if __name__ == '__main__':
    unittest.main()
