from pydantic import BaseModel


class MountPoint(BaseModel):
    """This is an abstraction on mount point of the storage"""

    name: str
    size: int
