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

### Tests
The `tests` directory contains unit tests to ensure the reliability and correctness of the application:

- `tests/protocol_tests.py`: Tests related to the message protocol.
- `tests/server_dummy.py`: A dummy server used for testing purposes.
- `tests/server_tests.py`: Tests related to the server functionality.
- `tests/test_frontend.py`: Tests related to the Flask frontend.
     - **test_home_page**: Validates that the home page is accessible and displays the correct content.
     - **test_token_submission**: Ensures that the token submission mechanism works correctly.
     - **test_error_page**: Checks if the error page can be accessed and shows the right content.
     - **test_reset_page**: Tests the password reset page's GET and POST operations to ensure proper functionality.
     - **test_invalid_email_submission**: Confirms that submitting an invalid email returns an error message.
     - **test_submit_edu_email**: Validates the behavior when a `.edu` email is submitted, expecting a successful operation.
     - **test_submit_non_edu_email**: Checks the behavior when a non-`.edu` email is submitted, expecting an error message.
     - **test_password_reset**: Validates that the password reset mechanism functions properly when provided with a token.



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

## Third Party Libraries
- `tomllib`: Used for parsing TOML configuration files.

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

## TODO

 - Implement basic server logic and frontend interaction.
 - Implement frontend tests.
 - Handle edge cases and exceptions in server-client communication.
 - Refactor frontend for better error handling.
 - Implement token-based authentication for added security.
 - Extend README with more detailed code examples and use cases.

## About

Password Reset Site is an initiative by LCC-CIT-Lab to provide a secure and straightforward way for users to reset their passwords. The project is open for contributions and welcomes feedback.

## Contact

- GitHub: @LCC-CIT-Lab
- Email: riddlej@lanecc.edu
