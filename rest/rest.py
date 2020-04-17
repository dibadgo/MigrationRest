import asyncio
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

from storage.mongo_provider import MongoDbProvider
from storage.repository import Repository
from migrations.migration import Migration, Workload, Credentials, \
    MountPoint, MigrationTarget
from handlers import request_exception_handler

from storage.workloads_repo import WorkloadsRepo

executor = ThreadPoolExecutor(4)

loop = asyncio.new_event_loop()
app = Flask(__name__)


@app.route("/")
def index():
    return "Hi, I'm ready!"


@app.route("/workloads", methods=['GET'])
@request_exception_handler
def get_workloads():
    repo = get_workload_repo()
    saved_workloads = loop.run_until_complete(repo.get_workloads_async())

    return jsonify([workload.to_dict() for workload in saved_workloads])


@app.route("/workloads/<workload_id>", methods=['GET'])
@request_exception_handler
def get_workload(workload_id):
    print(request)

    repo = get_workload_repo()
    workload = loop.run_until_complete(repo.get_workload_async(workload_id))

    return jsonify(workload.to_dict())


@app.route("/workloads", methods=['POST'])
@request_exception_handler
def create_workload():
    print(request)

    workload_params = _parse_workload_params(request.get_json())
    workload_params.pop('id')

    workload = Workload(**workload_params)
    repo = get_workload_repo()

    workload_id = loop.run_until_complete(repo.create_workload_async(workload))

    return "Workload was created successfully with id: {}".format(
        workload_id)


@app.route("/workloads", methods=['PUT'])
@request_exception_handler
def update_workload():
    repo = get_workload_repo()
    workload_params = _parse_workload_params(request.get_json())
    workload_id = workload_params['id']
    workload = loop.run_until_complete(repo.get_workload_async(workload_id))

    if workload_params['credentials']:
        workload.credentials = workload_params['credentials']
    if workload_params['mount_points']:
        workload.storage = workload_params['mount_points']

    loop.run_until_complete(repo.update_workload_async(workload_id, workload))
    return "Workload was updated successfully"


def _parse_workload_params(workload_dict):
    credentials_dict = workload_dict.get('Credentials')
    workload_credentials = None
    if credentials_dict:
        workload_credentials = Credentials(**credentials_dict)
    mount_points = None
    storage = workload_dict.get('Storage')
    if storage:
        mount_points = list(
            map(lambda x: MountPoint(x.get('name'), x.get('size')),
                storage))
    return {
        'id': workload_dict.get('id'),
        'ip': workload_dict.get('ip'),
        'credentials': workload_credentials,
        'mount_points': mount_points}


@app.route("/workloads", methods=['DELETE'])
@request_exception_handler
def delete_workload():
    workload_id = request.args.get('id')
    repo = get_workload_repo()

    loop.run_until_complete(repo.delete_workload_async(int(workload_id)))
    return "Workload was deleted successfully"


@app.route("/migrations", methods=['GET'])
@request_exception_handler
def get_migrations():
    repo = Repository()
    saved_migrations = repo.get_migrations()
    saved_migrations.pop('max_id')
    for migration_id in saved_migrations:
        saved_migrations[migration_id] = \
            saved_migrations[migration_id].to_dict()
    return str(saved_migrations)


@app.route("/migrations/state/<migration_id>", methods=['GET'])
@request_exception_handler
def get_migration_state(migration_id):
    repo = Repository()
    migration = repo.get_migration(int(migration_id))
    return migration.migration_state


@app.route("/migrations", methods=['POST'])
@request_exception_handler
def create_migration():
    migration_data = _parse_migration_params(request.get_json())
    repo = Repository()
    source_workload = \
        repo.get_workload(int(migration_data['source_id']))

    migration_target_data = migration_data['migration_target_params']
    target_workload = \
        repo.get_workload(int(migration_target_data['target_vm_id']))
    migration_target_data.pop('target_vm_id')

    migration_target = MigrationTarget(
        target_vm=target_workload,
        **migration_target_data)

    migration = Migration(mount_points=migration_data['mount_points'],
                          source=source_workload,
                          migration_target=migration_target)
    migration_id = repo.create_migration(migration)
    return "Migration created successfully with id: {}".format(
        migration_id)


@app.route("/migrations", methods=['PUT'])
@request_exception_handler
def update_migration():
    migration_data = _parse_migration_params(request.get_json())
    repo = Repository()

    migration = repo.get_migration(int(migration_data['id']))

    if migration_data['mount_points']:
        migration.mount_points = migration_data['mount_points']

    if migration_data['source_id']:
        source_workload = \
            repo.get_workload(int(migration_data['source_id']))
        migration.source = source_workload

    if migration_data['migration_target_params']:
        migration_target_data = migration_data['migration_target_params']

        if migration_target_data['target_vm_id']:
            target_workload = repo.get_workload(
                int(migration_target_data['target_vm_id']))
            migration.migration_target.target_vm = target_workload

        if migration_target_data['cloud_type']:
            migration.migration_target.cloud_type = \
                migration_target_data['cloud_type']

        if migration_target_data['cloud_credentials']:
            migration.migration_target.cloud_credentials = \
                migration_target_data['cloud_credentials']

    repo.update_migration(migration_data['id'], migration)

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
    repo = Repository()
    repo.delete_migration(int(migration_id))
    return "Migration was deleted successfully"


@app.route("/migrations/run", methods=['POST'])
@request_exception_handler
def run_migration():
    migration_id = int(request.args.get('id'))
    executor.submit(start_migration, migration_id)
    return "Migration {} started successfully".format(migration_id)


def start_migration(migration_id):
    repo = Repository()
    migration = repo.get_migration(migration_id)
    if migration.migration_state == 'RUNNING':
        print('Migration {} is already running!'.format(migration_id))
        return
    try:
        print('Starting migration {}'.format(migration_id))
        migration.migration_state = 'RUNNING'
        repo.update_migration(migration_id, migration)
        migration.run()
        migration.migration_state = 'SUCCESS'
        repo.update_migration(migration_id, migration)
        print('Migration completed successfully')
    except Exception as ex:
        print('Error while running migration {migration_id} : {error}'
              .format(migration_id=migration_id, error=ex))
        migration.migration_state = 'ERROR'
        repo.update_migration(migration_id, migration)


def get_workload_repo():
    asyncio.set_event_loop(loop)
    client = MongoDbProvider.obtain_client()
    return WorkloadsRepo(client)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001)
