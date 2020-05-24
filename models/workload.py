from models.mount_point import MountPoint
from models.credentials import Credentials


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