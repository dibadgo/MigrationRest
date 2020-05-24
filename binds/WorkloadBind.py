from typing import List, Optional
from pydantic import BaseModel
from models.mount_point import MountPoint
from models.credentials import Credentials
from models.workload import Workload


class WorkloadBind(BaseModel):
    """Bind model to configure a workload"""

    ip: str
    credentials: Optional[Credentials]
    storage: Optional[List[MountPoint]]

    def get_workload(self) -> Workload:
        if not self.credentials:
            raise Exception("Credentials should be defined")
        if self.storage is None:
            raise Exception("Storage should be defined")

        return Workload(id=None, ip=self.ip, credentials=self.credentials, storage=self.storage)
