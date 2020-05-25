import logging
from os import environ

from motor.motor_asyncio import AsyncIOMotorClient

from storage.migration_repo import MigrationRepo
from storage.workloads_repo import WorkloadsRepo


class RepoProvider:

    def __init__(self) -> None:
        self._workload_repo = None
        self._migration_repo = None
        self.client = self._create_motor_client_from_env()
        super().__init__()

    @property
    def workload_repo(self):
        if not self._workload_repo:
            self._workload_repo = self._create_workload_repo()

        return self._workload_repo

    @property
    def migration_repo(self):
        if not self._migration_repo:
            self._migration_repo = self._create_migration_repo()

        return self._migration_repo

    def _create_motor_client_from_env(self) -> AsyncIOMotorClient:
        """ Configure the Motor client for MongoDb from the environment variables

        :return: Motor client
        """
        username = environ.get("MM_MONGO_USR")
        password = environ.get("MM_MONGO_PASS")
        host = environ.get("MM_MONGO_HOST")
        port = environ.get("MM_MONGO_PORT")

        connection_string = f'mongodb://{username}:{password}@{host}:{port}'
        logging.debug(f"Mongo connection string {connection_string}")

        return AsyncIOMotorClient(f'mongodb://{username}:{password}@{host}:{port}')

    def _create_migration_repo(self) -> MigrationRepo:
        workload_repo = self.workload_repo
        return MigrationRepo(self.client, workload_repo)

    def _create_workload_repo(self) -> WorkloadsRepo:
        return WorkloadsRepo(self.client)


async def repos_provider() -> RepoProvider:
    return RepoProvider()
