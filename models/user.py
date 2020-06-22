from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None


class RegisterUser(User):
    password: str


class UserInDB(User):
    hashed_password: str
