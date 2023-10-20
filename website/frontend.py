import os
import toml
import socket
import datetime
import subprocess

from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from protocol import Lookup, message_builder, Update, Token, Success, Error, Email
from cryptography.fernet import Fernet, InvalidToken


# Function to load or create configuration
def load_or_create_config():
    config_file_path = 'config.toml'
    default_config = {
        'server': {
            'host': '0.0.0.0',
            'port': 5000,
            'unix_socket_path': '/tmp/unix_sock',
        },
        'app': {
            'token_expiry_seconds': 1800,
        },
        'smtp': {
            'host': 'localhost',
            'port': 1025,
            'from_address': 'no-reply@lanecc.edu'
        },
        'encryption': {
            'key': Fernet.generate_key().decode(),
        }
    }

    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as file:
            toml.dump(default_config, file)
            print(f'{config_file_path} created with default configurations.')

    with open(config_file_path, 'r') as file:
        config = toml.load(file)
        return config


# Load the configurations
config = load_or_create_config()


# Flask App Configuration
app = Flask(__name__, template_folder='../templates')
app.secret_key = Fernet.generate_key()


# Utility Functions
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message.decode()


def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
    return decrypted_message


def send_token_to_server(token):
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client_socket.connect('/tmp/unix_sock')
        client_socket.sendall(token.encode())
        response_str = client_socket.recv(1024).decode()
        return message_builder(response_str)
    finally:
        client_socket.close()


def send_new_password_to_server(concatenated_message):
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect(config['server']['unix_socket_path'])

        # Send the concatenated message to the server
        client_socket.sendall(concatenated_message.encode())

        # Receive server response and decode it
        response_str = client_socket.recv(1024).decode()
        response_message = message_builder(response_str)

        match response_message:
            case Success():
                return {'status': 'success'}
            case Error(error=response_message.error):
                return {'status': 'error', 'error_message': response_message.error}
            case _:
                return {'status': 'error', 'error_message': 'Unknown response type'}

    except Exception as e:
        return {'status': 'error', 'error_message': f'Unable to communicate with server: {e}'}
    finally:
        client_socket.close()


def validate_token(token):
    try:
        parsed_token = message_builder(token)  # Assumes token is a string in JSON format
        creation_time = parsed_token.data.get('creation_time')

        # Ensure creation_time is a datetime object before proceeding
        if not isinstance(creation_time, datetime.datetime):
            raise ValueError("creation_time is not a datetime object")

        delta = datetime.datetime.now() - creation_time

        if delta.total_seconds() > config['app']['token_expiry_seconds']:
            return False

        return True
    except (ValueError, KeyError, AttributeError) as e:
        print(f"Validation Error: {e}")  # Print the error to the console for debugging
        return False


def send_reset_link_to_user(email, link):
    try:
        # Create the email message
        subject = "LCC Password Reset"
        body = f"Dear User,\n\nPlease use the following link to reset your password:\n\n{link}\n\nThank you,\nLCC Support"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = config['smtp']['from_address']  # assuming this is still in your config
        msg['To'] = email

        # Write the email to a file
        with open('email.txt', 'w') as file:
            file.write(msg.as_string())

        # Send the email using msmtp
        command = f"cat email.txt | msmtp --account={config['smtp']['account']} -t"
        process = subprocess.Popen(command, shell=True)
        process.communicate()

        # Optionally, remove the email file after sending
        os.remove('email.txt')

    except Exception as e:
        print(f"Failed to send email: {e}")


# Flask Route Handlers
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']

    if not email.endswith('.edu'):
        flash('Please enter a valid .edu email address')
        return redirect(url_for('error'))

    # If it's a valid .edu email, proceed
    try:
        email_obj = Email(email)
        request_message = Lookup(email_obj)
        message = str(request_message)

        # Create a new socket object for communication
        client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client_socket.connect(config['server']['unix_socket_path'])
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        response_message = message_builder(response)

        match response_message:
            case Token():
                encrypted_token = encrypt_message(str(response_message), config['encryption']['key'].encode())
                reset_link = f"http://localhost:5000/reset?token={encrypted_token}"
                send_reset_link_to_user(email, reset_link)  # Send reset link to the user's email
                flash('Please check your email for a password reset link.')
                return redirect(url_for('thank_you'))  # Redirect to 'thank_you' page
            case Error(error=response_message.error):
                if response_message.error == "NOTFOUND":
                    # Email not found, skip sending reset link, but still redirect to 'thank_you' page
                    flash('Please check your email for a password reset link.')
                    return redirect(url_for('thank_you'))  # Redirect to 'thank_you' page
                else:
                    flash(f"Message: {str(response_message)}")
            case _:
                flash(f"Message: {str(response_message)}")

    except Exception as e:
        flash(f"Error communicating with the server: {e}")
        return redirect(url_for('error'))

    finally:
        client_socket.close()


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/submit_token', methods=['POST'])
def submit_token():
    token = request.form.get('token')

    if not validate_token(token):
        return redirect(url_for('error'))

    if request.method == 'POST':
        encrypted_token = request.form['token']

        try:
            decrypted_token = decrypt_message(encrypted_token, config['encryption']['key'].encode())
            response = send_token_to_server(decrypted_token)

            if response['status'] == 'error':
                error_msg = response.get('error_message')
                return render_template('error_token.html', error_message=error_msg)

            return render_template('success_token.html')

        except InvalidToken:
            return "Invalid token", 400

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    encrypted_token = request.args.get('token')

    # Decrypt token
    try:
        token = decrypt_message(encrypted_token, config['encryption']['key'].encode())
    except Exception as e:
        print(f"Decryption Error: {e}")
        flash("Invalid or expired reset link.")
        return redirect(url_for('error'))

    # Validate token
    if not validate_token(token):
        flash("Invalid or expired reset link.")
        return redirect(url_for('error'))

    if request.method == 'GET':
        return render_template('reset_page.html', token=encrypted_token)

    # Extract username from token
    try:
        parsed_token = message_builder(token)
        if parsed_token.message_type != "Token":  # Adjusted to match object attributes
            raise ValueError("Invalid token format.")
        username = parsed_token.username  # Adjusted to match object attributes
    except (ValueError, AttributeError):  # Adjusted the exception types
        print("Error: Invalid token format.")
        flash('Invalid token format.')
        return redirect(url_for('error'))

    # Handle POST request
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        flash('Passwords do not match!')
        return render_template('reset_page.html', token=encrypted_token)

    update_message = Update(username, new_password)
    response = send_new_password_to_server(str(update_message))

    if response['status'] == 'success':
        flash('Password reset successful!')
        return redirect(url_for('success'))
    else:
        flash(response['error_message'])
        return redirect(url_for('error'))


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(host=config['server']['host'], port=config['server']['port'])
