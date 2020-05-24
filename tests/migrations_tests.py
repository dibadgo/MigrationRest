import unittest

import models.credentials
import models.mount_point
import models.target
import models.workload
from models import migration


class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._mount_points = [models.mount_point.MountPoint('C:\\', 42)]
        cls._credentials = models.credentials.Credentials('User',
                                                 'passwrd',
                                                 'xxx.com')
        cls._test_workload = models.workload.Workload('111.11.11',
                                                      cls._credentials,
                                                      cls._mount_points)
        cls._test_migration_target = \
            models.target.MigrationTarget('vsphere',
                                          cls._credentials,
                                          cls._test_workload)

    def test_valid_migration(self):
        test_migration = \
            migration.Migration(self._mount_points,
                                self._test_workload,
                                self._test_migration_target)

        self.assertEqual(test_migration.mount_points,
                         self._mount_points)

        self.assertEqual(test_migration.source, self._test_workload)
        self.assertEqual(test_migration.migration_target,
                         self._test_migration_target)
        self.assertEqual(test_migration.migration_state, 'NOT_STARTED')

    def test_run_migration_without_c(self):
        self._mount_points[0].name = 'D:\\'
        test_migration = \
            migration.Migration(self._mount_points,
                                self._test_workload,
                                self._test_migration_target)

        with self.assertRaises(Exception):
            test_migration.run()

    def test_invalid_mountpoints(self):
        with self.assertRaises(Exception):
            migration.Migration(444,
                                self._test_workload,
                                self._test_migration_target)

    def test_invalid_source(self):
        with self.assertRaises(Exception):
            migration.Migration(self._mount_points,
                                '123',
                                self._test_migration_target)

    def test_invalid_migrationtarget(self):
        with self.assertRaises(Exception):
            migration.Migration(self._mount_points,
                                self._test_workload,
                                None)


class MigrationTargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mount_points = [models.mount_point.MountPoint('Good name', 42)]
        cls._credentials = models.credentials.Credentials('User',
                                                 'passwrd',
                                                 'xxx.com')
        cls._test_workload = models.workload.Workload('111.11.11',
                                                      cls._credentials,
                                                      mount_points)

    def test_valid_type_credentials_target(self):
        migration_target = models.target.MigrationTarget('vsphere',
                                                         self._credentials,
                                                         self._test_workload)

        self.assertEqual(migration_target.cloud_type, 'vsphere')
        self.assertEqual(migration_target.cloud_credentials,
                         self._credentials)
        self.assertEqual(migration_target.target_vm,
                         self._test_workload)

    def test_invalid_type(self):
        with self.assertRaises(Exception):
            models.target.MigrationTarget('some_bad_type',
                                          self._credentials,
                                          self._test_workload)

    def test_invalid_credentials(self):
        with self.assertRaises(Exception):
            models.target.MigrationTarget('azure', 42, self._test_workload)

    def test_invalid_target(self):
        with self.assertRaises(Exception):
            models.target.MigrationTarget('aws',
                                          self._credentials,
                                      'something_wrong')


class WorkloadTests(unittest.TestCase):
    def test_valid_ip_credentials_storage(self):
        credentials = models.credentials.Credentials('User',
                                            'passwrd',
                                            'xxx.com')
        mount_points = [models.mount_point.MountPoint('Good name', 42)]
        test_workload = models.workload.Workload('111.11.11',
                                                 credentials,
                                                 mount_points)
        self.assertEqual(test_workload.ip, '111.11.11')
        self.assertEqual(test_workload.credentials, credentials)
        self.assertEqual(test_workload.storage, mount_points)

    def test_attempt_to_change_ip(self):
        credentials = models.credentials.Credentials('User',
                                            'passwrd',
                                            'xxx.com')
        mount_points = [models.mount_point.MountPoint('Good name', 42)]
        test_workload = models.workload.Workload('111.11.11',
                                                 credentials,
                                                 mount_points)

        with self.assertRaises(Exception):
            test_workload.ip = 'New ip'

    def test_invalid_ip(self):
        credentials = models.credentials.Credentials('User',
                                            'passwrd',
                                            'xxx.com')
        mount_points = [models.mount_point.MountPoint('Good name', 42)]

        with self.assertRaises(Exception):
            models.workload.Workload(None, credentials, mount_points)

    def test_invalid_credentials(self):
        mount_points = [models.mount_point.MountPoint('Good name', 42)]

        with self.assertRaises(Exception):
            models.workload.Workload('111.11.11', None, mount_points)

    def test_invalid_storage(self):
        credentials = models.credentials.Credentials('User',
                                            'passwrd',
                                            'xxx.com')

        with self.assertRaises(Exception):
            models.workload.Workload('111.11.11', credentials, None)


class CredentialsTests(unittest.TestCase):
    def test_valid_usrname_password_domain(self):
        credentials = models.credentials.Credentials('User',
                                            'passwrd',
                                            'xxx.com')

        self.assertEqual(credentials.user_name, 'User')
        self.assertEqual(credentials.password, 'passwrd')
        self.assertEqual(credentials.domain, 'xxx.com')

    def test_invalid_username(self):
        with self.assertRaises(Exception):
            models.credentials.Credentials(None, 'passwrd', 'xxx.com')

    def test_invalid_password(self):
        with self.assertRaises(Exception):
            models.credentials.Credentials('usr', None, 'xxx.com')

    def test_invalid_domain(self):
        with self.assertRaises(Exception):
            models.credentials.Credentials('usr', 'passwrd', None)


class MountPointTests(unittest.TestCase):
    def test_valid_name_and_size(self):
        mount_point = models.mount_point.MountPoint('Good name', 42)

        self.assertEqual(mount_point.name, 'Good name')
        self.assertEqual(mount_point.size, 42)

    def test_invalid_name(self):
        with self.assertRaises(Exception):
            models.mount_point.MountPoint(423, 42)

    def test_invalid_size(self):
        with self.assertRaises(Exception):
            models.mount_point.MountPoint('Good name', 'bad size')


if __name__ == '__main__':
    unittest.main()