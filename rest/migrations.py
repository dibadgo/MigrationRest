import asyncio

from fastapi import APIRouter
from fastapi.params import Depends

from binds.MigrationBind import MigrationBind
from models.migration_manager import MigrationManager
from rest.dependencies import RepoProvider, repos_provider


router = APIRouter()
loop = asyncio.get_event_loop()


@router.get("/migrations/{migration_id}/state")
async def get_migration_state(migration_id, repos: RepoProvider = Depends(repos_provider)):
    """ Returns the migration state by Id

    :param repos: RepoProvider
    :param migration_id: Migration Id
    :return: MigrationState
    """
    repo = repos.migration_repo
    migration = await repo.get_async(migration_id)

    return migration.migration_state


@router.post("/migrations/{migration_id}/run")
def run_migration(migration_id, repos: RepoProvider = Depends(repos_provider)):
    """ Run the migration process in foreground

    :param repos: RepoProvider
    :param migration_id: Migration id
    :return: String message
    """
    repo = repos.migration_repo
    manager = MigrationManager(repo)
    coro = asyncio.ensure_future(manager.start_migration_async(migration_id), loop=loop)
    loop.run_until_complete(coro)

    return f"The migration {migration_id} started successfully"


@router.get("/migrations")
async def get_migrations(repos: RepoProvider = Depends(repos_provider)):
    """ Returns the migration model by Id

    :param repos: RepoProvider
    :return: Migration
    """
    repo = repos.migration_repo
    saved_migrations = await repo.list_async()
    return [m.to_dict() for m in saved_migrations]


@router.post("/migrations")
async def create_migration(bind: MigrationBind, repos: RepoProvider = Depends(repos_provider)):
    """ Creates the migration model by provided configuration

    :param bind: Migration configuration
    :param repos: RepoProvider
    :return: Migration model
    """
    migration_repo = repos.migration_repo

    created_migration = await migration_repo.create_async(bind)
    return created_migration


@router.patch("/migrations/{migration_id}")
async def update_migration(migration_id, bind: MigrationBind, repos: RepoProvider = Depends(repos_provider)):
    """ Modify the migration model

    :param migration_id: Migration id
    :param bind: New migration configuration
    :param repos: RepoProvider
    :return: Migration model
    """
    migration_repo = repos.migration_repo

    updated_migration = await migration_repo.update_async(migration_id, bind)

    return updated_migration


@router.delete("/migrations/{migration_id}")
async def delete_migration(migration_id: str, repos: RepoProvider = Depends(repos_provider)):
    """ Remove the migration model from Db

    :param migration_id: Migration Id
    :param repos: RepoProvider
    :return: Result message
    """
    repo = repos.migration_repo
    await repo.delete_async(migration_id)

    return "Migration was deleted successfully"
