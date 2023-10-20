import unittest
import cryptography

from unittest.mock import patch, Mock, MagicMock
from website.frontend import app
from protocol.protocol import Email


class FrontendTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the testing client for Flask.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        """
        Test if the home page is accessible without login.
        """
        response = self.client.get('/')
        self.assertIn(b'Enter your email to reset your password:', response.data)

    @patch('website.frontend.send_token_to_server')
    def test_token_submission(self, mock_send_token):
        mock_send_token.return_value = '{"status": "success", "token_data": {}}'
        response = self.client.post('/submit', data={'email': 'sample_email@domain.edu'})
        self.assertIn(b'Redirecting...', response.data)

    def test_error_page(self):
        response = self.client.get('/error')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error', response.data)

    @patch('website.frontend.validate_token')
    def test_reset_page(self, mock_validate_token):
        mock_validate_token.return_value = True
        response = self.client.get('/reset?gAAAAABlLxRbkczHq0OycQ53TYIaVgGsGtbRMJ9ots3JRvhozdxOOXKI6_MzgDEtV1ZYtj42BZ3rSCNaGusMWFGttTE5R9_5uS_yv87UTqEnCSDli1M0FN-EYHuwPogtYRyKAGon1glRgQSsBjJIJGUIyGJKB_j7G-3a6UD8F5Udtgiu-bOAQBZzScyya8wNmQ2Cr7Ffnpd-rxMwEWLU8MGTJPmBrM7ZIivseMvUHFO-o7M3lfiI9Kp63YMJVYC3i2XNQBYhlp16')
        self.assertEqual(response.status_code, 302)

    @patch('website.frontend.message_builder')
    @patch('socket.socket')
    def test_invalid_email_submission(self, mock_socket, mock_message_builder):
        mock_socket_instance = Mock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b'{"message_type": "Error", "error": "Invalid email"}'
        mock_response = Mock()
        mock_response.message_type = 'Error'
        mock_response.error = "Invalid email"
        mock_message_builder.return_value = mock_response
        response = self.client.post('/submit', data={'email': 'invalid_email'}, follow_redirects=True)
        self.assertIn(b'Error', response.data)

    @patch('website.frontend.Lookup')  # Mock the Lookup class from protocol.py
    @patch('website.frontend.message_builder')  # Mock the message_builder function from protocol.py
    @patch('socket.socket')  # Mock the socket.socket class from the socket module
    def test_submit_edu_email(self, mock_socket, mock_message_builder, mock_lookup):
        """
        Test the /submit route with a valid .edu email, mocking external dependencies.
        """

        # Set up the mock Lookup instance
        mock_lookup_instance = MagicMock(name="Lookup Instance")
        mock_lookup.return_value = mock_lookup_instance
        mock_lookup_instance.__str__.return_value = '{"username": "test@lanecc.edu"}'

        # Set up the mock socket instance
        mock_socket_instance = Mock(name="Socket Instance")
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b'{"message_type": "Success"}'

        # Set up the mock message_builder function
        mock_response = Mock(name="Response Object")  # This represents a Response object
        mock_response.message_type = 'Success'
        mock_message_builder.return_value = mock_response

        # Make a POST request
        response = self.client.post('/submit', data={'email': 'test@lanecc.edu'}, follow_redirects=True)

        # Assert that the response contains the expected data
        self.assertIn(b'', response.data)

        # Check whether Lookup is instantiated with the correct arguments
        mock_lookup.assert_called_once()
        assert isinstance(mock_lookup.call_args[0][0], Email)
        assert mock_lookup.call_args[0][0].address == 'test@lanecc.edu'

        # Check whether the socket methods are called with expected arguments
        mock_socket_instance.connect.assert_called_once_with('/tmp/unix_sock')
        mock_socket_instance.sendall.assert_called_once_with(b'{"username": "test@lanecc.edu"}')

        # Check that message_builder is called with the expected arguments
        mock_message_builder.assert_called_once_with('{"message_type": "Success"}')

        # Additional assertions can be added here to verify other aspects of the /submit route's behavior

    @patch('website.frontend.Lookup')  # Mock the Lookup class from protocol.py
    @patch('website.frontend.message_builder')  # Mock the message_builder function from protocol.py
    @patch('socket.socket')  # Mock the socket.socket class from the socket module
    def test_submit_non_edu_email(self, mock_socket, mock_message_builder, mock_lookup):
        """
        Test the /submit route with a non-.edu email, expecting an error message.
        """
        # Set up the mock Lookup instance
        mock_lookup_instance = MagicMock(name="Lookup Instance")
        mock_lookup.return_value = mock_lookup_instance
        mock_lookup_instance.__str__.return_value = '{"email": "test@lanecc.com"}'

        # Set up the mock socket instance
        mock_socket_instance = Mock(name="Socket Instance")
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b'{"message_type": "Error"}'

        # Set up the mock message_builder function
        mock_response = Mock(name="Response Object")  # This represents a Response object
        mock_response.message_type = 'Error'
        mock_message_builder.return_value = mock_response

        # Make a POST request
        response = self.client.post('/submit', data={'email': 'test@lanecc.com'}, follow_redirects=True)
        self.assertIn(b'Error', response.data)

    def test_password_reset(self):
        client = app.test_client()
        response = client.post('/reset?token=gAAAAABlLxT2hKOp3qnhWZ7DzGyKW3jVW4pKYfTXrLf6AaTwMQlrXbzchPGDBzeDQUwiVb0XADSRM4HIYQad0XBSBIaqDM-Y61f4kkmdxixkW6G9RidsCOvI7J7Ot6NLKXIQwyLKSifRr2hHOJTAYY1Q61BjURAFacBDu4rb0jPEl-fXpDtV-ZM5EOepH_BL4VyI98eah3zcnwF36iof2wQhxjyBDVczyojq0Prqf_xcQP2WL1cl4FkpACpIVboUoR0-q78unTQL',
                               data={'new_password': 'newPass123', 'confirm_password': 'newPass123'},
                               follow_redirects=True)
        print(response.data)
        self.assertEqual(response.status_code, 200)  # Check if it's a successful response

    def test_mismatched_passwords(self):
        response = self.client.post('/reset/sample_token',
                                    data={'new_password': 'password1', 'confirm_password': 'password2'},
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    @patch('website.frontend.decrypt_message')
    @patch('website.frontend.send_token_to_server')
    def test_invalid_token_submission(self, mock_send_token, mock_decrypt_message):
        mock_send_token.return_value = '{"status": "error", "message": "Invalid token"}'
        mock_decrypt_message.side_effect = cryptography.fernet.InvalidToken
        response = self.client.post('/submit_token', data={'token': 'invalid_token'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirection

    def test_successful_email_without_edu(self):
        response = self.client.post('/submit', data={'email': 'test@notedu.com'}, follow_redirects=True)
        # Assuming you want to check for not successful submission:
        self.assertIn(b'Error', response.data)

    @patch('website.frontend.send_token_to_server')
    def test_token_timeout(self, mock_send_token):
        mock_send_token.return_value = '{"status": "error", "message": "Token has expired"}'
        response = self.client.post('/submit', data={'token': 'expired_token'})
        self.assertEqual(response.status_code, 400)

    def test_edge_cases_email_submission(self):
        response = self.client.post('/submit', data={'email': 'test..test@lanecc.edu'}, follow_redirects=True)
        self.assertIn(b'Reset Your Password', response.data)


if __name__ == '__main__':
    unittest.main()
