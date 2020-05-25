import logging

from models.state import MigrationState
from storage.migration_repo import MigrationRepo


class MigrationManager:
    """Manage of migration logic"""

    def __init__(self, migration_repo: MigrationRepo) -> None:
        self._migration_repo = migration_repo
        super().__init__()

    async def start_migration_async(self, migration_id):
        """ Run the migration process

        :param migration_id: Migration id
        """
        migration = await self._migration_repo.get_async(migration_id)

        if migration.migration_state != MigrationState.NOT_STARTED:
            logging.error(f'The migration {migration_id} should be in NOT_STARTED state')
            return

        try:
            logging.info(f'Starting migration {migration_id}')
            migration.migration_state = MigrationState.RUNNING
            await self._migration_repo.save_migration_async(migration)

            migration.run()

            migration.migration_state = MigrationState.SUCCESS
            await self._migration_repo.save_migration_async(migration)
            logging.info(f'The migration {migration_id} completed successfully')
        except Exception as ex:
            logging.error(f'Error while running migration {migration_id} : {ex}')
            migration.migration_state = MigrationState.ERROR
            await self._migration_repo.save_migration_async(migration)
