from typing import List, Optional
from pydantic import BaseModel
from models.mount_point import MountPoint
from models.credentials import Credentials


class Workload(BaseModel):

    id: Optional[str]
    ip: str
    credentials: Credentials
    storage: List[MountPoint]

    def to_dict(self):
        return self.dict(include={'id', 'ip', 'credentials', 'storage'})
