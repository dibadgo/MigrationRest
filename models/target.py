from models.clouds import CloudType
from models.credentials import Credentials
from models.workload import Workload


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