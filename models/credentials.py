from pydantic import BaseModel


class Credentials(BaseModel):
    user_name: str
    password: str
    domain: str
