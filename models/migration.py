import os
from time import sleep
from typing import List, Optional

from pydantic import BaseModel

from models.mount_point import MountPoint
from models.state import MigrationState
from models.target import MigrationTarget
from models.workload import Workload


class Migration(BaseModel):
    """The migration abstraction described the migration parameters and logic"""

    id: Optional[str]
    mount_points: List[MountPoint]
    source = Workload
    migration_target = MigrationTarget
    migration_state = MigrationState.NOT_STARTED

    def run(self, duration_mins=5):
        """ Start the migration process

        Basically the migration process is about
        copy the specified storage (mount points) from source Workload to target.
        We will delay some minutes to simulate the longer operation here.

        :param duration_mins: The numbers of minutes to delay
        """
        if self.is_running():
            raise RuntimeError("Transaction is already running!")

        migration_file_name = self._get_filename()
        try:
            sleep(duration_mins * 60)
            open(migration_file_name, 'a').close()

            if 'c:\\' not in \
                    map(lambda p: p.name.lower(), self.mount_points):
                raise RuntimeError(
                    'Allowed mounting points should contain C:\\!')

            if self.mount_points != \
                    self.migration_target.target_vm.storage:
                raise RuntimeError('Migration target should contain'
                                   ' only allowed mounting points!')

            sleep(duration_mins * 60)
        finally:
            if os.path.exists(migration_file_name):
                os.remove(migration_file_name)

    def is_running(self):
        """ Check that the migration process is in running state

        :return: Bool
        """
        return os.path.exists(self._get_filename())

    def to_dict(self):
        """ Convert the migration model to dict

        :return: dict
        """
        return self.dict(include={'id', 'mount_points', 'source', 'migration_target', 'migration_state'})

    def _get_filename(self):
        """ Make the migration filename (migration lock file)

        :return: migration filename
        """
        return f'{self.id}.migration'
