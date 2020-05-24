from typing import Optional, List
from pydantic import BaseModel
from binds.TargetBind import TargetBind
from models.migration import Migration
from models.mount_point import MountPoint

from models.workload import Workload


class MigrationBind(BaseModel):
    """Bind model to create or update the migration model"""

    id: Optional[str]
    mount_points: Optional[List[MountPoint]]
    source_id: str
    migration_target: TargetBind

    def get_migration(self, source_workload: Workload, target_workload: Workload) -> Migration:
        target = self.migration_target.get_target(target_workload)

        return Migration(
            id=self.id,
            mount_points=self.mount_points,
            source=source_workload,
            migration_target=target
        )
