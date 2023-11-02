# Password Reset Site

## Overview
This project is a secure password reset system that allows users to reset their passwords through a web interface. It's implemented in Python using the Flask framework for the frontend and a custom server setup for handling requests and responses.

## Getting Started

1. Clone the repository:

```
git clone https://github.com/LCC-CIT-Lab/password-reset-site.git
cd password-reset-site
pip install -r requirements.txt
```

2. Set the PYTHONPATH environment variable:
```
export PYTHONPATH=$PYTHONPATH:~/Documents/password-reset-site
```

3. Start the server:
```
python3 server/server.py
```

4. In a new terminal, launch the Flask application:
```
python3 site/frontend.py
```

5. Install and configure msmtp
```
sudo apt install msmtp
nano ~/.msmtprc

# Set default values for all following accounts.
defaults
auth           off
tls            off
logfile        ~/.msmtp.log

# Local SMTP Server
account        myapp
host           localhost
port           25
from           no-reply@lanecc.edu

# Set a default account
account default : myapp
```

## Project Structure

- `protocol/protocol.py`: Provides message classes used by `server.py` to format requests and responses.
- `server/server.py`: Hosts the server logic, including connection handling and argument parsing.
- `site/frontend.py`: Houses the Flask application for the frontend.

### Templates
The `templates` directory contains HTML templates used by the Flask application to render the web interface:

- `templates/error.html`: Displayed when a generic error occurs.
- `templates/error_token.html`: Displayed when there's an error related to the token.
- `templates/home.html`: The main homepage where users input their email for password reset.
- `templates/reset_page.html`: The page where users input their new password.
- `templates/success.html`: Displayed when a user successfully submits their email.
- `templates/success_token.html`: Displayed when a token operation is successful.
- `templates/thank_you.html`: Displayed when a user successfully submits their email.

### Tests
The `tests` directory contains unit tests to ensure the reliability and correctness of the application:

- `tests/protocol_tests.py`: Tests related to the message protocol.
- `tests/server_dummy.py`: A dummy server used for testing purposes.
- `tests/server_tests.py`: Tests related to the server functionality.
- `tests/test_frontend.py`: Tests related to the Flask frontend.

## Configurations
The server provides multiple configuration options, either via command line arguments or via a TOML-based configuration file. These include:
- Token Time-to-Live (TTL)
- Log level
- Log file location
- Socket file location
- Socket file owners
- Socket file permissions

Use a configuration file for consistent setups, and command line arguments for one-off or override settings.

## Technologies
- Python 3.11+
- Flask for the frontend
- UNIX Sockets for server-client communication

## Dependencies
- Flask for web application development
- `tomllib` for TOML configuration parsing
- `msmtp` for e-mail sending

## Third Party Libraries
- `tomllib`: Used for parsing TOML configuration files.
- `msmtp`: Used for emailing the reset token.

## Examples

### Making a Lookup Request using the Protocol
```
from protocol import Lookup, Email
email_obj = Email("test@lanecc.edu")
lookup_request = Lookup(email_obj)
```
### Handling a Response using the Protocol
```
from protocol import message_builder
response = '{"message_type": "Success"}'
response_message = message_builder(response)
```

## Commands & Options

The server can be started with multiple command line arguments to control its behavior, such as --log-level to set the logging level or --config to specify a configuration file path.

For a complete list of commands and options, refer to the server.py and its argparse setup.

## Testing

Frontend testing has been set up using Python's unittest module. Tests cover the main routes and interactions of the Flask application. To run the tests, execute:
```
python -m unittest tests/test_frontend.py
```

## About

Password Reset Site is an initiative by LCC-CIT-Lab to provide a secure and straightforward way for users to reset their passwords. The project is open for contributions and welcomes feedback.

## Contact

- GitHub: @LCC-CIT-Lab
- Email: CITLab@lanecc.edu
