import unittest

from models.clouds import CloudType
from models.mount_point import MountPoint
from models.credentials import Credentials
from models.state import MigrationState
from models.workload import Workload
from models.target import MigrationTarget
from models.migration import Migration


class MigrationTests(unittest.TestCase):
    """Test general models behavior"""

    @classmethod
    def setUpClass(cls):
        """Setup general models for each test"""
        cls._mount_points = [MountPoint(name='C:\\', size=42)]
        cls._credentials = Credentials(
            user_name='User',
            password='passwrd',
            domain='xxx.com'
        )
        cls._test_workload = Workload(
            id=None,
            ip='111.11.11',
            credentials=cls._credentials,
            storage=cls._mount_points
        )
        cls._test_migration_target = MigrationTarget(
            cloud_type=CloudType.VSPHERE,
            cloud_credentials=cls._credentials,
            target_vm=cls._test_workload
        )

    def test_valid_migration(self):
        """Test general properties of the migration model"""
        test_migration = Migration(
            mount_points=self._mount_points,
            source=self._test_workload,
            migration_target=self._test_migration_target,
            migration_state=MigrationState.NOT_STARTED
        )

        self.assertEqual(test_migration.mount_points, self._mount_points)
        self.assertEqual(test_migration.source, self._test_workload)
        self.assertEqual(test_migration.migration_target, self._test_migration_target)
        self.assertEqual(test_migration.migration_state, MigrationState.NOT_STARTED)

    def test_run_migration_without_c(self):
        """ Test migration without main mount point (C:\\ drive in this case)"""
        self._mount_points[0].name = 'D:\\'
        test_migration = Migration(
            mount_points=self._mount_points,
            source=self._test_workload,
            migration_target=self._test_migration_target,
            migration_state=MigrationState.NOT_STARTED
        )

        with self.assertRaises(Exception):
            test_migration.run()

    def test_run_migration_which_is_in_running_state(self):
        """ Test run the migration which is already in running state"""
        test_migration = Migration(
            mount_points=self._mount_points,
            source=self._test_workload,
            migration_target=self._test_migration_target,
            migration_state=MigrationState.RUNNING
        )

        with self.assertRaises(Exception):
            test_migration.run()

    def test_invalid_mountpoints(self):
        """Test create the migration model with invalid type of mount points"""
        with self.assertRaises(Exception):
            Migration(
                mount_points=444,
                source=self._test_workload,
                migration_target=self._test_migration_target,
                migration_state=MigrationState.RUNNING
            )

    def test_invalid_source(self):
        """Test create the migration model with invalid type of source Workload"""
        with self.assertRaises(Exception):
            Migration(
                mount_points=self._mount_points,
                source=111,
                migration_target=self._test_migration_target,
                migration_state=MigrationState.RUNNING
            )

    def test_invalid_migrationtarget(self):
        """Test create the migration model with invalid type of migration target"""
        with self.assertRaises(Exception):
            Migration(
                mount_points=self._mount_points,
                source=self._test_workload,
                migration_target=111,
                migration_state=MigrationState.RUNNING
            )


class MigrationTargetTests(unittest.TestCase):
    """Tests of the MigrationTarget model behavior"""

    @classmethod
    def setUpClass(cls):
        """Describe default models needs testing"""
        cls._mount_points = [MountPoint(name='C:\\', size=42)]
        cls._credentials = Credentials(
            user_name='User',
            password='passwrd',
            domain='xxx.com'
        )
        cls._test_workload = Workload(
            id=None,
            ip='111.11.11',
            credentials=cls._credentials,
            storage=cls._mount_points
        )

    def test_valid_type_credentials_target(self):
        """Test Target with correct models"""
        migration_target = MigrationTarget(
            cloud_type=CloudType.VSPHERE,
            cloud_credentials=self._credentials,
            target_vm=self._test_workload
        )

        self.assertEqual(migration_target.cloud_type, CloudType.VSPHERE)
        self.assertEqual(migration_target.cloud_credentials,
                         self._credentials)
        self.assertEqual(migration_target.target_vm,
                         self._test_workload)

    def test_invalid_type(self):
        """Test invalid cloud type"""
        with self.assertRaises(Exception):
            MigrationTarget(
                cloud_type="Invalid cloud type",
                cloud_credentials=self._credentials,
                target_vm=self._test_workload
            )

    def test_invalid_credentials(self):
        """Test invalid cloud credentials"""
        with self.assertRaises(Exception):
            MigrationTarget(
                cloud_type=CloudType.VSPHERE,
                cloud_credentials="Invalid type",
                target_vm=self._test_workload
            )

    def test_invalid_target(self):
        """Test invalid target Workload"""
        with self.assertRaises(Exception):
            MigrationTarget(
                cloud_type=CloudType.VSPHERE,
                cloud_credentials=self._credentials,
                target_vm="Some bad type"
            )


class WorkloadTests(unittest.TestCase):
    """Workload tests"""

    def test_valid_ip_credentials_storage(self):
        mount_points = [MountPoint(name='C:\\', size=42)]
        credentials = Credentials(
            user_name='User',
            password='passwrd',
            domain='xxx.com'
        )
        test_workload = Workload(
            id=None,
            ip='111.11.11',
            credentials=credentials,
            storage=mount_points
        )
        self.assertEqual(test_workload.ip, '111.11.11')
        self.assertEqual(test_workload.credentials, credentials)
        self.assertEqual(test_workload.storage, mount_points)

    def test_invalid_ip(self):
        mount_points = [MountPoint(name='C:\\', size=42)]
        credentials = Credentials(
            user_name='User',
            password='passwrd',
            domain='xxx.com'
        )

        with self.assertRaises(Exception):
            Workload(
                id=None,
                ip=None,
                credentials=credentials,
                storage=mount_points
            )

    def test_invalid_credentials(self):
        mount_points = [MountPoint(name='C:\\', size=42)]

        with self.assertRaises(Exception):
            Workload(
                id=None,
                ip="1.1.1.1",
                credentials=None,
                storage=mount_points
            )

    def test_invalid_storage(self):
        credentials = Credentials(
            user_name='User',
            password='passwrd',
            domain='xxx.com'
        )

        with self.assertRaises(Exception):
            Workload(
                id=None,
                ip="1.1.1.1",
                credentials=credentials,
                storage=None
            )


class CredentialsTests(unittest.TestCase):
    """Test for Credentials model"""

    def test_valid_usrname_password_domain(self):
        """Test with valid parameters"""
        credentials = Credentials(
            user_name='User',
            password='passwrd',
            domain='xxx.com'
        )

        self.assertEqual(credentials.user_name, 'User')
        self.assertEqual(credentials.password, 'passwrd')
        self.assertEqual(credentials.domain, 'xxx.com')

    def test_invalid_username(self):
        """Test with invalid username"""
        with self.assertRaises(Exception):
            Credentials(
                user_name=None,
                password='passwrd',
                domain='xxx.com'
            )

    def test_invalid_password(self):
        """Test with invalid password"""
        with self.assertRaises(Exception):
            Credentials(
                user_name="username",
                password=None,
                domain='xxx.com'
            )

    def test_invalid_domain(self):
        """Test with invalid domain"""
        with self.assertRaises(Exception):
            Credentials(
                user_name="username",
                password='passwrd',
                domain=None
            )


class MountPointTests(unittest.TestCase):
    """Test of MountPoint model"""

    def test_valid_name_and_size(self):
        """Test on valid parameters"""
        mount_point = MountPoint(name='C:\\', size=42)

        self.assertEqual(mount_point.name, 'C:\\')
        self.assertEqual(mount_point.size, 42)

    def test_invalid_name(self):
        """Test with invalid name"""
        with self.assertRaises(Exception):
            MountPoint(name=None, size=42)

    def test_invalid_size(self):
        with self.assertRaises(Exception):
            MountPoint(name='Good name', size='bad size')


if __name__ == '__main__':
    unittest.main()