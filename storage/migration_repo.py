from storage.repository import Repository


class MigrationRepo(Repository):
    def create_migration(self, migration):
        self._start_transaction(self._migrations_path)
        try:
            migrations = \
                self._read_entities_from_file(self._migrations_path)
            new_migration_id = migrations['max_id']
            migrations[new_migration_id] = migration
            migrations['max_id'] += 1
            self._save_entities_to_file(migrations,
                                        self._migrations_path)
            return new_migration_id
        finally:
            self._end_transaction(self._migrations_path)

    def get_migration(self, migration_id):
        try:
            migrations = Repository._read_entities_from_file(
                self._migrations_path)
            return migrations[migration_id]
        except IndexError:
            raise RuntimeError('Migration with id: {} does not exist!'
                               .format(migration_id))

    def get_migrations(self):
        self._start_transaction(self._migrations_path)
        try:
            migrations = Repository._read_entities_from_file(
                self._migrations_path)
            return migrations
        finally:
            self._end_transaction(self._migrations_path)

    def update_migration(self, migration_id, migration):
        self._start_transaction(self._migrations_path)
        try:
            migrations = self._read_entities_from_file(
                self._migrations_path)
            if migration_id not in migrations:
                raise RuntimeError(
                    'Migration with id {} does not exist!'
                        .format(migration_id))
            migrations[migration_id] = migration
            self._save_entities_to_file(migrations,
                                        self._migrations_path)
        finally:
            self._end_transaction(self._migrations_path)

    def delete_migration(self, migration_id):
        self._start_transaction(self._migrations_path)
        try:
            migrations = Repository._read_entities_from_file(
                self._migrations_path)
            if migration_id not in migrations:
                raise RuntimeError('Workload with id {} does not exist!'
                                   .format(migration_id))
            migrations.pop(migration_id)
            self._save_entities_to_file(migrations,
                                        self._migrations_path)
        finally:
            self._end_transaction(self._migrations_path)

    @staticmethod
    def _read_entities_from_file(file_name):
        try:
            entities = {'max_id': 0}
            entities_exist = os.path.isfile(file_name)
            if entities_exist:
                with open(file_name, 'rb') as stored_entities:
                    entities = pickle.load(stored_entities)
                    entities['max_id'] = \
                        entities.get('max_id', len(entities))
            return entities
        except Exception as ex:
            print('Error while trying to read data from disk!')
            raise ex

    @staticmethod
    def _save_entities_to_file(entities, file_name):
        try:
            with open(file_name, 'wb') as stored_entities:
                pickle.dump(entities, stored_entities)
        except Exception as ex:
            print('Error while trying to save data on disk!')
            raise ex

    def _start_transaction(self, file_name):
        try:
            lock = FileLock(file_name + '.lock', timeout=600)
            lock.acquire()
            self.locks[file_name] = lock
        except Timeout as t_ex:
            print('Could not acquire file lock! '
                  'There probably is a dead process or thread')
            raise t_ex

    def _end_transaction(self, file_name):
        try:
            lock = self.locks.get(file_name)
            if lock:
                lock.release()
                self.locks.pop(file_name)
        except Exception as ex:
            print("""Could not release file lock! 
                    File still may be locked! Please check the existence 
                    of .lock files ({})"""
                  .format(file_name + 'lock'))
            raise ex

    WORKLOADS_FILE = 'workloads.data'

    MIGRATIONS_FILE = 'migrations.data'