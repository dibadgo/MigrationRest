import os
from enum import Enum
from time import sleep

from mongoengine import Document


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


class MigrationTarget:
    def __init__(self, cloud_type, cloud_credentials, target_vm):
        self.cloud_type = cloud_type
        self.cloud_credentials = cloud_credentials
        self.target_vm = target_vm

    @property
    def cloud_type(self):
        return self._cloud_type

    @cloud_type.setter
    def cloud_type(self, new_cloud_type):
        if new_cloud_type not in \
                [cloud_type.value for cloud_type in CloudType]:
            raise RuntimeError(
                'cloud_type should be of aws, azure, vsphere, vcloud')

        self._cloud_type = new_cloud_type

    @property
    def cloud_credentials(self):
        return self._cloud_credentials

    @cloud_credentials.setter
    def cloud_credentials(self, new_cloud_credentials):
        if not isinstance(new_cloud_credentials, Credentials):
            raise RuntimeError(
                'cloud_credentials should be of Credentials type!')

        self._cloud_credentials = new_cloud_credentials

    @property
    def target_vm(self):
        return self._target_vm

    @target_vm.setter
    def target_vm(self, new_target_vm):
        if not isinstance(new_target_vm, Workload):
            raise RuntimeError('target_vm should be of type Workload!')

        self._target_vm = new_target_vm

    def to_dict(self):
        return {
            'cloud_type': self.cloud_type,
            'cloud_credentials': self.cloud_credentials.__dict__}

    def __eq__(self, other):
        return self.cloud_type == other.cloud_type and \
               self.cloud_credentials == other.cloud_credentials and \
               self.target_vm == other.target_vm


class CloudType(Enum):
    AWS = 'aws'
    AZURE = 'azure'
    VSPHERE = 'vsphere'
    VCLOUD = 'vcloud'


class MigrationState(Enum):
    NOT_STARTED = 'NOT_STARTED'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'


class Workload:

    def __init__(self, ip, credentials, mount_points):
        if not isinstance(ip, str):
            raise RuntimeError('ip should be a string!')
        self._id = None
        self._ip = ip
        self.credentials = credentials
        self.storage = mount_points

    @property
    def id(self):
        return self._id

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, new_ip):
        raise RuntimeError('ip change is not allowed!')

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, new_credentials):
        if not isinstance(new_credentials, Credentials):
            raise RuntimeError(
                'credentials should be of Credentials type!')

        self._credentials = new_credentials

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, new_storage):
        if not new_storage:
            raise RuntimeError('Storage should not be null!')
        if not all(
                map(lambda m: isinstance(m, MountPoint), new_storage)):
            raise RuntimeError(
                'storage should contain a list of MountPoints!')

        self._storage = new_storage

    def to_dict(self):
        dict_repr = {
            'ip': self._ip,
            "Credentials": self._credentials.__dict__,
            'Storage': list(map(lambda mp: mp.__dict__, self._storage))}
        return dict_repr

    def __eq__(self, other):
        return self.ip == other.ip and \
               self.credentials == other.credentials and \
               self.storage == other.storage


class Credentials:
    def __init__(self, user_name, password, domain):
        self.user_name = user_name
        self.password = password
        self.domain = domain

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, new_name):
        if not isinstance(new_name, str):
            raise RuntimeError('user_name should be a string!')

        self._user_name = new_name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        if not isinstance(new_password, str):
            raise RuntimeError('password should be a string!')

        self._password = new_password

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, new_domain):
        if not isinstance(new_domain, str):
            raise RuntimeError('domain should be a string!')

        self._domain = new_domain

    def __eq__(self, other):
        return self.user_name == other.user_name and \
               self.password == other.password and \
               self.domain == other.domain


class MountPoint:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise RuntimeError('name should be a string!')

        self._name = new_name

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        if not isinstance(new_size, int):
            raise RuntimeError('size should be an int!')

        self._size = new_size

    def __eq__(self, other):
        return self.name == other.name and self.size == other.size
