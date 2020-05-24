from dataclasses import dataclass
from models.clouds import CloudType
from models.credentials import Credentials


@dataclass
class TargetBind:
    """Bind model to describe the target cloud and workload"""

    target_vm_id: str
    cloud_credentials: Credentials
    cloud_type: CloudType
