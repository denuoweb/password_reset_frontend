# Password Reset Site

## Overview
This project is a secure password reset system allowing users to reset their passwords through a web interface. It's implemented in Python using the Flask framework for the frontend, and a custom server setup for handling requests and responses.

## Project Structure
- `protocol/protocol.py` (Message Protocol): Provides message classes used by server.py to format requests and responses and for processing.
- `server/server.py` (Server Logic): Hosts the server logic, including connection handling and argument parsing. Processes requests from frontend.py. Formats messages using classes from protocol.py. Sends responses back to frontend.py.
- `site/frontend.py` (Flask Application): Houses the Flask application for the frontend. Sends requests to and receives responses from server.py. Renders the web interface for users.

## Prerequisites
- Python 3.8+
- Flask

## Installation
1. Clone the repository:  
```git clone https://github.com/LCC-CIT-Lab/password-reset-site.git```  
```cd password-reset-site```  
```pip install -r requirements.txt```  

## Usage
1. Start the server:  
```python3 server/server.py```

2. In a new terminal, launch the Flask application:  
```python3 site/frontend.py```

## Contact
    GitHub: @LCC-CIT-Lab
    Email: riddlej@lanecc.edu
