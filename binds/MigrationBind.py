from binds import TargetBind
from models.mount_point import MountPoint
from dataclasses import dataclass


@dataclass
class MigrationBind:
    """Bind model to create or update the migration model"""

    id: str
    mount_points: [MountPoint]
    source_id: str
    migration_target: TargetBind
