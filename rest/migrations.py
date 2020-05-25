import asyncio
import logging

from fastapi import APIRouter

from binds.MigrationBind import MigrationBind
from models.state import MigrationState
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
    workloads_repo = _get_workload_repo()
    migration_repo = _get_migration_repo()

    source_workload = await workloads_repo.get_async(bind.source_id)
    target_workload = await workloads_repo.get_async(bind.migration_target.target_vm_id)

    migration = bind.get_migration(source_workload, target_workload)

    created_migration = await migration_repo.create_async(migration)
    return created_migration


@router.patch("/migrations/{migration_id}")
async def update_migration(migration_id, bind: MigrationBind):
    """ Modify the migration model

    :param migration_id: Migration id
    :param bind: New migration configuration
    :return: Migration model
    """
    workloads_repo = _get_workload_repo()
    migration_repo = _get_migration_repo()

    migration = await migration_repo.get_async(migration_id)

    if bind.mount_points:
        migration.mount_points = bind.mount_points

    if bind.source_id:
        source_workload = await workloads_repo.get_async(bind.source_id)
        migration.source = source_workload

    if bind.migration_target:
        if bind.migration_target.target_vm_id:
            target_workload = await workloads_repo.get_async(bind.migration_target.target_vm_id)
            migration.migration_target.target_vm = target_workload

        if bind.migration_target.cloud_type:
            migration.migration_target.cloud_type = bind.migration_target.cloud_type

        if bind.migration_target.cloud_credentials:
            migration.migration_target.cloud_credentials = bind.migration_target.cloud_credentials

    updated_migration = await migration_repo.update_async(migration_id, migration)

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


@router.post("/migrations/run/{migration_id}")
def run_migration(migration_id):
    """ Run the migration process in foreground

    :param migration_id: Migration id
    :return: Message
    """
    coro = asyncio.ensure_future(_start_migration_logic(migration_id), loop=loop)
    loop.run_until_complete(coro)

    return "Migration {} started successfully".format(migration_id)


async def _start_migration_logic(migration_id):
    """ Run the migration process

    :param migration_id: Migration id
    """
    repo = _get_migration_repo()
    migration = await repo.get_async(migration_id)
    if migration.migration_state == MigrationState.RUNNING:
        logging.error(f'Migration {migration_id} is already running!')
        return

    try:
        logging.info(f'Starting migration {migration_id}')
        migration.migration_state = MigrationState.RUNNING
        await repo.update_async(migration_id, migration)

        migration.run()

        migration.migration_state = MigrationState.SUCCESS
        await repo.update_async(migration_id, migration)
        logging.info(f'The migration {migration_id} completed successfully')
    except Exception as ex:
        logging.error(f'Error while running migration {migration_id} : {ex}')
        migration.migration_state = MigrationState.ERROR
        await repo.update_async(migration_id, migration)


def _get_migration_repo():
    client = MotorClientFactory.create_from_env()
    return MigrationRepo(client)


def _get_workload_repo():
    client = MotorClientFactory.create_from_env()
    return WorkloadsRepo(client)
