from pydantic import BaseModel


class Credentials(BaseModel):
    """The model of cloud credentials"""

    user_name: str
    password: str
    domain: str
