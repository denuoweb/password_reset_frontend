import json
from datetime import datetime


def _validate(**kwargs) -> None:
    for key in kwargs.items():
        if len(key) > 256:
            raise ValueError("{} is longer than 256 characters".format(key))


class Email:
    def __init__(self, email: str):
        _validate(email=email)
        self._address: str | None = None
        size = email.count('@')
        if size > 1 or size == 0:
            raise TypeError("Not a valid address")
        elif domain := email.split('@')[1] != "my.lancc.edu":
            if domain != "lanecc.edu":
                raise TypeError("Not a valid address")

        self._address = email

    @property
    def address(self):
        return self._address


class Message:
    def __init__(self):
        self._message_type = type(self).__name__

    @property
    def message_type(self):
        return self._message_type


# Message Types
class Request(Message):
    def __init__(self, username: str):
        super().__init__()
        _validate(username=username)
        self._username = username

    @property
    def username(self):
        return self._username

    def __str__(self):
        return json.dumps({
            'message_type': self.message_type,
            'username': self.username,
        })


class Response(Message):
    def __init__(self, **kwargs):
        super().__init__()
        _validate(**kwargs)
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
        super().__init__(username)
        _validate(password=password)
        self._password = password

    @property
    def password(self):
        return self._password

    def __str__(self):
        return json.dumps({'message_type': self.message_type, 'username': self.username, 'password': self.password})


# Response Types
class Token(Response):
    def __init__(self, username: str, creation_time: datetime, email: Email):
        super().__init__(username=username, creation_time=creation_time, email=email)

    @property
    def creation_time(self):
        return self.data['creation_time']

    @property
    def username(self):
        return self.data['username']

    @property
    def email(self):
        return self.data['email'].address

    def __str__(self):
        time = self.creation_time.isoformat()
        return json.dumps(
            {"message_type": self.message_type, "username": self.username, "creation_time": time, "email": self.email})


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

    if 'message_type' not in json_dict:
        raise TypeError("Not a Message")

    match json_dict['message_type']:
        case 'Lookup':
            message = Lookup(json_dict['username'])
        case 'Update':
            message = Update(json_dict['username'], json_dict['password'])
        case 'Token':
            time = datetime.fromisoformat(json_dict['creation_time'])
            email = Email(json_dict['email'])
            message = Token(json_dict['username'], creation_time=time, email=email)
        case 'Success':
            message = Success()
        case 'Error':
            message = Error(json_dict['error'])
        case _:
            raise TypeError("Unknown Message type")

    return message
