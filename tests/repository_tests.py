import os
import unittest
from storage.repository import Repository
from migrations import migration


class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._mount_points = [migration.MountPoint('Good name', 42)]
        cls._credentials = migration.Credentials('User',
                                                 'passwrd',
                                                 'xxx.com')
        cls._test_workload = migration.Workload('111.11.11',
                                                cls._credentials,
                                                cls._mount_points)
        cls._test_migration_target = \
            migration.MigrationTarget('vsphere',
                                      cls._credentials,
                                      cls._test_workload)
        cls._test_migration = \
            migration.Migration(cls._mount_points,
                                cls._test_workload,
                                cls._test_migration_target)
        cls._repo = Repository()

    def setUp(self):
        self.clear_files()

    def tearDown(self):
        self.clear_files()

    def clear_files(self):
        if os.path.exists('workloads.data'):
            os.remove('workloads.data')
        if os.path.exists('migrations.data'):
            os.remove('migrations.data')

    def test_create_workload(self):
        w_id = self._repo.create_workload(self._test_workload)

        restored_workload = self._repo.get_workload(w_id)

        self.assertEqual(self._test_workload, restored_workload)

    def test_create_workload_with_existing_ip(self):
        with self.assertRaises(Exception):
            self._repo.create_workload(self._test_workload)
            self._repo.create_workload(self._test_workload)

    def test_update_existing_workload(self):
        w_id = self._repo.create_workload(self._test_workload)
        self._test_workload.credentials.user_name = 'New User'

        self._repo.update_workload(w_id, self._test_workload)

        updated_workload = self._repo.get_workload(w_id)
        self.assertEqual(self._test_workload, updated_workload)

    def test_update_not_existing_workload(self):
        with self.assertRaises(Exception):
            self._repo.update_workload(-42, self._test_workload)

    def test_delete_workloads(self):
        workloads = self._repo.get_workloads()
        workloads.pop('max_id')
        for workload_id in workloads:
            self._repo.delete_workload(workload_id)

        workloads = self._repo.get_workloads()
        workloads.pop('max_id')
        self.assertEqual(len(workloads), 0)

    def test_delete_not_existing_workload(self):
        with self.assertRaises(Exception):
            self._repo.delete_workload(-42)

    def test_create_migration(self):
        m_id = self._repo.create_migration(self._test_migration)

        restored_migration = self._repo.get_migration(m_id)

        self.assertEqual(self._test_migration, restored_migration)

    def test_update_existing_migration(self):
        m_id = self._repo.create_migration(self._test_migration)

        self._test_migration.migration_target.cloud_credentials\
            .user_name = 'New test user name'
        self._repo.update_migration(m_id, self._test_migration)

        restored_migration = self._repo.get_migration(m_id)
        self.assertEqual(self._test_migration, restored_migration)

    def test_update_not_existing_migration(self):
        with self.assertRaises(Exception):
            self._repo.update_migration(-42, self._test_migration)

    def test_delete_migration(self):
        with self.assertRaises(Exception):
            self._repo.delete_migration(-42)


if __name__ == '__main__':
    unittest.main()
