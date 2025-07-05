from ninja import Schema


class RegisterSchema(Schema):
    username: str
    password: str

class LoginSchema(Schema):
    username: str
    password: str

class UserOut(Schema):
    id: int
    username: str