from pydantic import BaseModel

from models.clouds import CloudType
from models.credentials import Credentials
from models.target import MigrationTarget
from models.workload import Workload


class TargetBind(BaseModel):
    """Bind model to describe the target cloud and workload"""

    target_vm_id: str
    cloud_credentials: Credentials
    cloud_type: CloudType

    def get_target(self, target_workload: Workload) -> MigrationTarget:
        return MigrationTarget(
            cloud_type=self.cloud_type,
            cloud_credentials=self.cloud_credentials,
            target_vm=target_workload
        )
