import socketserver
import socket
import os
import logging
import json
import urllib.parse  # Add this import
import re  # Importing regex module for email validation

from datetime import datetime, timedelta
from protocol import Lookup, Update, message_builder, Token, Email, Success, Error

# Setting up logging
logging.basicConfig(level=logging.INFO)

if os.path.exists("/tmp/unix_sock"):
    os.remove("/tmp/unix_sock")


def is_valid_token(token_str, username):
    try:
        token_data = json.loads(token_str)

        # Check for required keys in token
        required_keys = ['message_type', 'username', 'creation_time', 'email']
        if not all(key in token_data for key in required_keys):
            return False

        # Check if message_type is "Token"
        if token_data['message_type'] != 'Token':
            return False

        # Check if the username matches
        if token_data['username'] != username:
            return False

        # Check if the token's creation_time is within the last 30 minutes
        token_time = datetime.fromisoformat(token_data['creation_time'])
        if datetime.now() - token_time > timedelta(minutes=30):
            return False

        return True
    except Exception as e:
        logging.error(f"Token validation error: {e}")
        return False


class MyUnixStreamHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = None  # Initialize data attribute

        try:
            logging.info("Waiting for data from client...")
            self.data = self.request.recv(1024).strip()
            logging.info("Raw received data: %s", self.data)

            # Check if data is empty
            if not self.data:
                logging.error("Received empty data from client.")
                response = Error("No data received from client.").__str__()
                self.request.sendall(response.encode('utf-8'))
                return

            # Convert byte data to string
            data_str = self.data.decode('utf-8')
            logging.info("Decoded received data: %s", data_str)

            # Check if the message contains the delimiter indicating it's a concatenated message
            if "||TOKEN||" in data_str:
                # Split the data into parts using the delimiter "||TOKEN||"
                parts = data_str.split("||TOKEN||")

                # Extract the token and message
                if len(parts) != 2:
                    response = Error("Invalid message format.").__str__()
                    self.request.sendall(response.encode('utf-8'))
                    return

                token_str, message_str = parts

                # Validate the token
                if not is_valid_token(token_str, ""):  # Pass an empty username for now
                    response = Error("Invalid token.").__str__()
                    self.request.sendall(response.encode('utf-8'))
                    return

                received_message = message_builder(message_str)
            else:
                received_message = message_builder(data_str)

            if isinstance(received_message, Lookup):
                logging.info("Received Lookup Message with email: %s", received_message.email)

                # Validate email format
                email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
                if not email_regex.match(received_message.email):
                    response = Error("email address not valid").__str__()
                elif "rosenauj@my.lanecc.edu" in received_message.email:
                    token_response = Token(username="L00653400", creation_time=datetime.now(),
                                           email=Email(received_message.email))
                    response = token_response.__str__()
                else:
                    response = Error("NOTFOUND").__str__()

            elif isinstance(received_message, Update):
                logging.info(
                    f"Update message received. Username: {received_message.username}, Password: {received_message.password}")
                response = Success().__str__()

            else:
                response = Error("Unexpected message type received").__str__()

            logging.info("Sending response: %s", response)  # Log the response being sent
            self.request.sendall(response.encode('utf-8'))

        except BrokenPipeError:
            logging.error("Client closed the connection before the server could respond.")
            return

        except Exception as e:
            logging.error("Error: %s", e)
            response = Error("Please contact admin at CITLab@lanecc.edu").__str__()
            self.request.sendall(response.encode('utf-8'))

        finally:
            # Properly close the connection after sending the data
            self.request.shutdown(socket.SHUT_RDWR)
            self.request.close()


if __name__ == "__main__":
    server = socketserver.UnixStreamServer('/tmp/unix_sock', MyUnixStreamHandler)
    logging.info("Server running...")
    server.serve_forever()
