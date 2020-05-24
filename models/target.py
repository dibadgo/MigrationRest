from pydantic import BaseModel

from models.clouds import CloudType
from models.credentials import Credentials
from models.workload import Workload


class MigrationTarget(BaseModel):
    """The model to describe the migration target"""

    cloud_type: CloudType
    cloud_credentials: Credentials
    target_vm: Workload

    def to_dict(self):
        return self.dict(include={"cloud_type", "cloud_credentials"})
