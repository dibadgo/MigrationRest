
@app.route("/migrations", methods=['POST'])
@request_exception_handler
def create_migration(bind: MigrationBind):
    migration_data = _parse_migration_params(request.get_json())

    workloads_repo = get_workload_repo()
    migration_repo = get_migration_repo()
    source_workload = \
        loop.run_until_complete(workloads_repo.get_async(migration_data['source_id']))

    migration_target_data = migration_data['migration_target_params']

    target_workload = \
        loop.run_until_complete(workloads_repo.get_async(migration_target_data['target_vm_id']))
    migration_target_data.pop('target_vm_id')

    migration_target = MigrationTarget(
        target_vm=target_workload,
        **migration_target_data)

    migration = Migration(mount_points=migration_data['mount_points'],
                          source=source_workload,
                          migration_target=migration_target)
    migration_id = loop.run_until_complete(migration_repo.create_async(migration))
    return "Migration created successfully with id: {}".format(
        migration_id)


@app.route("/migrations/<migration_id>", methods=['PUT'])
@request_exception_handler
def update_migration(migration_id):
    migration_data = _parse_migration_params(request.get_json())

    workload_repo = get_workload_repo()
    migration_repo = get_migration_repo()

    migration = loop.run_until_complete(migration_repo.get_async(migration_id))

    if migration_data['mount_points']:
        migration.mount_points = migration_data['mount_points']

    if migration_data['source_id']:
        source_workload = \
            loop.run_until_complete(workload_repo.get_async(migration_data['source_id']))
        migration.source = source_workload

    if migration_data['migration_target_params']:
        migration_target_data = migration_data['migration_target_params']

        if migration_target_data['target_vm_id']:
            target_workload = loop.run_until_complete(workload_repo.get_async(
                migration_target_data['target_vm_id']))
            migration.migration_target.target_vm = target_workload

        if migration_target_data['cloud_type']:
            migration.migration_target.cloud_type = \
                migration_target_data['cloud_type']

        if migration_target_data['cloud_credentials']:
            migration.migration_target.cloud_credentials = \
                migration_target_data['cloud_credentials']

    loop.run_until_complete(migration_repo.update_async(migration_id, migration))

    return "Migration updated successfully"


def _parse_migration_params(migration_dict):
    mount_points = migration_dict.get('mount_points')
    if mount_points:
        mount_points = list(map(
            lambda x: MountPoint(x.get('name'), x.get('size')),
            mount_points))
    migration_target_params = _parse_migration_target_params(
        migration_dict.get('migration_target'))
    return {'id': migration_dict.get('id'),
            'mount_points': mount_points,
            'source_id': migration_dict.get('source_id'),
            'migration_target_params': migration_target_params}


def _parse_migration_target_params(migration_target_dict):
    cloud_credentials = None
    if 'cloud_credentials' in migration_target_dict:
        cloud_credentials = \
            Credentials(**migration_target_dict['cloud_credentials'])
    return {'cloud_type': migration_target_dict.get('cloud_type'),
            'cloud_credentials': cloud_credentials,
            'target_vm_id': migration_target_dict.get('target_vm_id')}


@app.route("/migrations", methods=['DELETE'])
@request_exception_handler
def delete_migration():
    migration_id = request.args.get('id')
    repo = get_migration_repo()
    loop.run_until_complete(repo.delete_async(migration_id))
    return "Migration was deleted successfully"


@app.route("/migrations/run/<migration_id>", methods=['POST'])
@request_exception_handler
def run_migration(migration_id):
    # asyncio.create_task(greet_every_two_seconds())  # Only in Python 3.8
    executor.submit(start_migration, migration_id)
    return "Migration {} started successfully".format(migration_id)


def start_migration(migration_id):
    """ Run the migration process

    :param migration_id: Migration id
    """
    repo = get_migration_repo()
    migration = loop.run_until_complete(repo.get_async(migration_id))
    if migration.migration_state == 'RUNNING':
        print('Migration {} is already running!'.format(migration_id))
        return
    try:
        print('Starting migration {}'.format(migration_id))
        migration.migration_state = 'RUNNING'
        loop.run_until_complete(repo.update_async(migration_id, migration))
        migration.run()
        migration.migration_state = 'SUCCESS'
        loop.run_until_complete(repo.update_async(migration_id, migration))
        print('Migration completed successfully')
    except Exception as ex:
        print('Error while running migration {migration_id} : {error}'
              .format(migration_id=migration_id, error=ex))
        migration.migration_state = 'ERROR'
        loop.run_until_complete(repo.update_async(migration_id, migration))

