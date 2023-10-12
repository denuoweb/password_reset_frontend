import unittest
import json
from datetime import datetime
from protocol import Email, Request, Response, Lookup, Update, Token, Success, Error, message_builder


class TestProtocol(unittest.TestCase):
    def test_email_valid(self):
        # Test a valid email address
        email = Email("test@my.lanecc.edu")
        self.assertEqual(email.address, "test@my.lanecc.edu")
        email = Email("test@lanecc.edu")
        self.assertEqual(email.address, "test@lanecc.edu")

    def test_email_invalid(self):
        # Test an invalid email address
        with self.assertRaises(TypeError):
            Email("invalid_email")

    def test_request_serialization(self):
        # Test serialization of Request
        request = Request()
        expected_json = '{"message_type": "Request"}'
        self.assertEqual(str(request), expected_json)

    def test_response_serialization(self):
        # Test serialization of Response
        response = Response(error="An error message")
        expected_json = '{"message_type": "Response", "error": "An error message"}'
        self.assertEqual(str(response), expected_json)

    def test_lookup_request_serialization(self):
        # Test serialization of Lookup Request
        email = Email('example@lanecc.edu')
        lookup_request = Lookup(email)
        expected_json = '{"message_type": "Lookup", "email": "example@lanecc.edu"}'
        self.assertEqual(str(lookup_request), expected_json)

    def test_update_request_serialization(self):
        # Test serialization of Update Request
        update_request = Update("testuser", "newpassword")
        expected_json = '{"message_type": "Update", "username": "testuser", "password": "newpassword"}'
        self.assertEqual(str(update_request), expected_json)

    def test_token_response_serialization(self):
        # Test serialization of Token Response
        creation_time = datetime(2023, 1, 1, 0, 0, 0)
        email = Email("test@lanecc.edu")
        token_response = Token("testuser", creation_time, email)
        expected_json = '{"message_type": "Token", "username": "testuser", "creation_time": "2023-01-01T00:00:00", "email": "test@lanecc.edu"}'
        self.assertEqual(str(token_response), expected_json)

    def test_success_response_serialization(self):
        # Test serialization of Success Response
        success_response = Success()
        expected_json = '{"message_type": "Success"}'
        self.assertEqual(str(success_response), expected_json)

    def test_error_response_serialization(self):
        # Test serialization of Error Response
        error_response = Error("An error message")
        expected_json = '{"message_type": "Error", "error": "An error message"}'
        self.assertEqual(str(error_response), expected_json)

    def test_message_builder(self):
        # Test Lookup Request
        lookup_json = '{"message_type": "Lookup", "email": "example@lanecc.edu"}'
        lookup_message = message_builder(lookup_json)
        self.assertIsInstance(lookup_message, Lookup)
        self.assertEqual(lookup_message.email, "example@lanecc.edu")

        # Test Update Request
        update_json = '{"message_type": "Update", "username": "testuser", "password": "newpassword"}'
        update_message = message_builder(update_json)
        self.assertIsInstance(update_message, Update)
        self.assertEqual(update_message.username, "testuser")
        self.assertEqual(update_message.password, "newpassword")

        # Test Token Response
        token_json = '{"message_type": "Token", "username": "testuser", "creation_time": "2023-01-01T00:00:00", "email": "test@lanecc.edu"}'
        token_message = message_builder(token_json)
        self.assertIsInstance(token_message, Token)
        self.assertEqual(token_message.username, "testuser")
        self.assertEqual(token_message.email, "test@lanecc.edu")

        # Test Success Response
        success_json = '{"message_type": "Success"}'
        success_message = message_builder(success_json)
        self.assertIsInstance(success_message, Success)

        # Test Error Response
        error_json = '{"message_type": "Error", "error": "An error message"}'
        error_message = message_builder(error_json)
        self.assertIsInstance(error_message, Error)
        self.assertEqual(error_message.error, "An error message")

        # Test invalid message type
        invalid_json = '{"message_type": "InvalidType"}'
        with self.assertRaises(TypeError):
            message_builder(invalid_json)

        # Test missing message type
        missing_type_json = '{"username": "testuser"}'
        with self.assertRaises(TypeError):
            message_builder(missing_type_json)


if __name__ == '__main__':
    unittest.main()
