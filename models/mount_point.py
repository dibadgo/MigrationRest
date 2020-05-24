from pydantic import BaseModel


class MountPoint(BaseModel):
    name: str
    size: int
