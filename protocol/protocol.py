import json
from datetime import datetime


class Message:
    def __init__(self):
        self.message_type = type(self).__name__


# Message Types
class Request(Message):
    def __init__(self, username: str, password: str = None):
        super().__init__()
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    def __str__(self):
        return json.dumps({
            'message_type': self.message_type,
            'username': self.username,
            'password': self._password
        })


class Response(Message):
    def __init__(self, **kwargs):
        super().__init__()
        self.message_type = type(self).__name__
        self.data = kwargs

    def __str__(self):
        return json.dumps({
            'message_type': self.message_type,
            **self.data
        })


# Request Types
class Lookup(Request):
    def __init__(self, username: str):
        super().__init__(username)


class Update(Request):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    @property
    def password(self):
        return self._password


# Response Types
class Token(Response):
    def __init__(self, username: str, creation_time: datetime):
        super().__init__(username=username, creation_time=creation_time)

    @property
    def creation_time(self):
        return self.data['creation_time']

    @property
    def username(self):
        return self.data['username']

    def __str__(self):
        token_datetime = self.creation_time
        day = token_datetime.day
        month = token_datetime.month
        year = token_datetime.year
        hour = token_datetime.hour
        minute = token_datetime.minute
        second = token_datetime.second

        return json.dumps(
            {'message_type': self.message_type, 'username': self.username, 'day': day, 'month': month, 'year': year,
             'hour': hour, 'minute': minute, 'second': second})


class Success(Response):
    def __init__(self):
        super().__init__()


class Error(Response):
    def __init__(self, error: str):
        super().__init__(error=error)

    @property
    def error(self):
        return self.data['error']


def message_builder(json_str: str) -> Message:
    json_dict = json.loads(json_str)
    message = None

    match json_dict['message_type']:
        case 'Lookup':
            message = Lookup(json_dict['username'])
        case 'Update':
            message = Update(json_dict['username'], json_dict['password'])
        case 'Token':
            message = Token(json_dict['username'], json_dict['creation_time'])
        case 'Success':
            message = Success()
        case 'Error':
            message = Error(json_dict['error'])

    return message
