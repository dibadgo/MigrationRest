from dataclasses import dataclass
from migrations.migration import Credentials, CloudType


@dataclass
class TargetBind:
    """Bind model to describe the target cloud and workload"""

    target_vm_id: str
    cloud_credentials: Credentials
    cloud_type: CloudType
