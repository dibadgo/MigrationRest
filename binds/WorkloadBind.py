from dataclasses import dataclass
from typing import List
from pydantic import BaseModel
from migrations.migration import Credentials, MountPoint



class Credentials1(BaseModel):
    user_name: str
    password: str
    domain: str


class MountPoint1(BaseModel):
    name: str
    size: int



class WorkloadBind(BaseModel):
    """Bind model to configure a workload"""

    ip: str
    credentials: Credentials1
    storage: List[MountPoint1]


