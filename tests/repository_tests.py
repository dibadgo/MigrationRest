import unittest
from unittest.mock import MagicMock
import asyncio

from models.clouds import CloudType
from models.credentials import Credentials
from models.migration import Migration
from models.mount_point import MountPoint
from models.state import MigrationState
from models.target import MigrationTarget
from models.workload import Workload
from storage.cruid_repository import CruidRepository


TEST_OBJECT_ID = "5e9b1c836ca6be564403c673"


class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        cls._test_migration = Migration(
            mount_points=cls._mount_points,
            source=cls._test_workload,
            migration_target=cls._test_migration_target,
            migration_state=MigrationState.NOT_STARTED
        )
        cls.results_mock = CollectionResults()

    def setUp(self):
        self.results_mock = CollectionResults()

    def _make_collections(self):

        insert_execute_coro = asyncio.coroutine(self.results_mock.insert_res)
        find_execute_coro = asyncio.coroutine(self.results_mock.find_res)
        replace_execute_coro = asyncio.coroutine(self.results_mock.replace_res)
        counts_doc_execute_coro = asyncio.coroutine(self.results_mock.count_res)
        removed_execute_coro = asyncio.coroutine(self.results_mock.remove_res)

        collection_mock = MagicMock()
        collection_mock.insert_one = insert_execute_coro
        collection_mock.replace_one = replace_execute_coro
        collection_mock.find_one = find_execute_coro
        collection_mock.count_documents = counts_doc_execute_coro
        collection_mock.delete_many = removed_execute_coro

        return collection_mock

    def _make_motor_client(self):
        db_mock = MagicMock()
        d = {'test_collection': self._make_collections()}
        db_mock.__getitem__.side_effect = d.__getitem__
        db_mock.__iter__.side_effect = d.__iter__

        motor_mock = MagicMock()
        motor_mock.mig_database = db_mock
        return motor_mock

    def test_create_document(self):

        async def run_test():
            motor_mock = self._make_motor_client()
            repo = CruidRepository(motor_mock, "test_collection")
            inserted_id = await repo.create_async(self._test_workload)

            assert self.results_mock.find_res == inserted_id.id

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_test())

    def test_update_existing_document(self):

        async def run_test():
            motor_mock = self._make_motor_client()
            repo = CruidRepository(motor_mock, "test_collection")
            inserted_id = await repo._replace_document("5e9b1c836ca6be564403c673", self._test_workload)

            assert 1 == inserted_id.modified_count

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_test())

    def test_update_not_existing_document(self):

        async def run_test():
            replace_result_mock = MagicMock()
            replace_result_mock.modified_count = 0

            self.results_mock.replace_res = MagicMock(return_value=replace_result_mock)

            motor_mock = self._make_motor_client()
            repo = CruidRepository(motor_mock, "test_collection")

            inserted_id = await repo._replace_document("5e9b1c836ca6be564403c673", self._test_workload)

            assert 0 == inserted_id.modified_count

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_test())

    def test_delete_document(self):

        async def run_test():
            motor_mock = self._make_motor_client()
            repo = CruidRepository(motor_mock, "test_collection")

            inserted_id = await repo.delete_async("5e9b1c836ca6be564403c673")

            assert 1 == inserted_id

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_test())

    def test_delete_not_existing_document(self):

        async def run_test():
            remove_result_mock = MagicMock()
            remove_result_mock.side_effect = Exception()

            self.results_mock.remove_res = remove_result_mock

            motor_mock = self._make_motor_client()
            repo = CruidRepository(motor_mock, "test_collection")

            with self.assertRaises(Exception):
                await repo.delete_async("5e9b1c836ca6be564403c673")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_test())


class CollectionResults:

    def __init__(self, **kwargs):
        self.insert_res = kwargs.get("insert_res", self._default_insert_mock())
        self.find_res = kwargs.get("find_res", self._default_find_mock())
        self.replace_res = kwargs.get("replace_res", self._default_replace_mock())
        self.count_res = kwargs.get("count_res", self._default_count_mock())
        self.remove_res = kwargs.get("remove_res", self._default_remove_mock())

    @staticmethod
    def _default_remove_mock():
        return MagicMock()

    @staticmethod
    def _default_count_mock():
        count_docs_mock = MagicMock()
        count_docs_mock.side_effect = [3, 2]
        return count_docs_mock

    @staticmethod
    def _default_replace_mock():
        replace_result_mock = MagicMock()
        replace_result_mock.modified_count = 1

        return MagicMock(return_value=replace_result_mock)

    @staticmethod
    def _default_find_mock():
        document_id = MagicMock()
        document_id.id = TEST_OBJECT_ID

        return document_id

    @staticmethod
    def _default_insert_mock():
        document_id = MagicMock()
        document_id.inserted_id = TEST_OBJECT_ID

        return MagicMock(return_value=document_id)


if __name__ == '__main__':
    unittest.main()
