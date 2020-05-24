import os
from time import sleep

from models.mount_point import MountPoint
from models.state import MigrationState
from models.target import MigrationTarget
from models.workload import Workload


class Migration:
    def __init__(self, mount_points, source, migration_target):
        self.mount_points = mount_points
        self.source = source
        self.migration_target = migration_target
        self.migration_state = 'NOT_STARTED'

    @property
    def mount_points(self):
        return self._mount_points

    @mount_points.setter
    def mount_points(self, points):
        if not points:
            raise RuntimeError('Mount points should not be empty!')
        if not all(map(lambda mp: isinstance(mp, MountPoint), points)):
            raise RuntimeError(
                'All mount points should be of type MountPoint!')
        self._mount_points = points

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, new_source):
        if not isinstance(new_source, Workload):
            raise RuntimeError(
                'Migration Source should be of type Workload!')
        self._source = new_source

    @property
    def migration_target(self):
        return self._migration_target

    @migration_target.setter
    def migration_target(self, new_migration_target):
        if not isinstance(new_migration_target, MigrationTarget):
            raise RuntimeError(
                'migration_target should be of type MigrationTarget!')
        self._migration_target = new_migration_target

    @property
    def migration_state(self):
        return self._migration_state

    @migration_state.setter
    def migration_state(self, new_migration_state):
        if new_migration_state not in \
                [migr_state.value for migr_state in MigrationState]:
            raise RuntimeError('migration_state should be of '
                               'NOT_STARTED, RUNNING, ERROR, SUCCESS')
        self._migration_state = new_migration_state

    def run(self, duration_mins=5):
        if self.is_running():
            raise RuntimeError("Transaction is already running!")

        migration_file_name = str(hash(self)) + '.migration'
        try:
            open(migration_file_name, 'a').close()

            if 'c:\\' not in \
                    map(lambda p: p.name.lower(), self._mount_points):
                raise RuntimeError(
                    'Allowed mounting points should contain C:\\!')

            if self._mount_points != \
                    self.migration_target.target_vm.storage:
                raise RuntimeError('Migration target should contain'
                                   ' only allowed mounting points!')

            sleep(duration_mins * 60)
        finally:
            if os.path.exists(migration_file_name):
                os.remove(migration_file_name)

    def is_running(self):
        migration_file_name = str(hash(self)) + '.migration'
        return os.path.exists(migration_file_name)

    def to_dict(self):
        points_dicts = \
            list(map(lambda mp: mp.__dict__, self.mount_points))
        dict_repr = {
            'mount_points': points_dicts,
            'source': self.source.to_dict(),
            'migration_target': self.migration_target.to_dict(),
            "migration_state": self.migration_state}
        return dict_repr

    def __hash__(self):
        h = hash("{}.{}".format(
            self.source.ip,
            self._migration_target.target_vm.ip))
        return h

    def __eq__(self, other):
        return self.mount_points == other.mount_points and \
               self.source == other.source and \
               self.migration_target == other.migration_target and \
               self.migration_state == other.migration_state


