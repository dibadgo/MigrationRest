import asyncio

from fastapi import APIRouter

from binds.MigrationBind import MigrationBind
from models.migration_manager import MigrationManager
from storage.migration_repo import MigrationRepo
from storage.mongo_provider import MotorClientFactory
from storage.workloads_repo import WorkloadsRepo


router = APIRouter()
loop = asyncio.get_event_loop()


@router.get("/migrations/state/{migration_id}")
async def get_migration_state(migration_id):
    """ Returns the migration state by Id

    :param migration_id: Migration Id
    :return: MigrationState
    """
    repo = _get_migration_repo()
    migration = await repo.get_async(migration_id)

    return migration.migration_state


@router.post("/migrations/run/{migration_id}")
def run_migration(migration_id):
    """ Run the migration process in foreground

    :param migration_id: Migration id
    :return: String message
    """
    repo = _get_migration_repo()
    manager = MigrationManager(repo)
    coro = asyncio.ensure_future(manager.start_migration_async(migration_id), loop=loop)
    loop.run_until_complete(coro)

    return f"The migration {migration_id} started successfully"


@router.get("/migrations")
async def get_migrations():
    """ Returns the migration model by Id

    :return: Migration
    """
    repo = _get_migration_repo()
    saved_migrations = await repo.list_async()
    return [m.to_dict() for m in saved_migrations]


@router.post("/migrations")
async def create_migration(bind: MigrationBind):
    """ Creates the migration model by provided configuration

    :param bind: Migration configuration
    :return: Migration model
    """
    migration_repo = _get_migration_repo()

    created_migration = await migration_repo.create_async(bind)
    return created_migration


@router.patch("/migrations/{migration_id}")
async def update_migration(migration_id, bind: MigrationBind):
    """ Modify the migration model

    :param migration_id: Migration id
    :param bind: New migration configuration
    :return: Migration model
    """
    migration_repo = _get_migration_repo()

    updated_migration = await migration_repo.update_async(migration_id, bind)

    return updated_migration


@router.delete("/migrations/{migration_id}")
async def delete_migration(migration_id: str):
    """ Remove the migration model from Db

    :param migration_id: Migration Id
    :return: Result message
    """
    repo = _get_migration_repo()
    await repo.delete_async(migration_id)

    return "Migration was deleted successfully"


def _get_migration_repo() -> MigrationRepo:
    client = MotorClientFactory.create_from_env()
    workload_repo = _get_workload_repo(client)
    return MigrationRepo(client, workload_repo)


def _get_workload_repo(client=None) -> WorkloadsRepo:
    if not client:
        client = MotorClientFactory.create_from_env()
    return WorkloadsRepo(client)
