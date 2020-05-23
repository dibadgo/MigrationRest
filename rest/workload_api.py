import asyncio
from main import app
from rest.handlers import request_exception_handler
from storage.migration_repo import MigrationRepo
from storage.mongo_provider import MotorClientFactory
from migrations.migration import Workload, Credentials, MountPoint
from storage.workloads_repo import WorkloadsRepo


@app.route("/")
def index():
    return "Hi, I'm ready!"


@app.route("/workloads", methods=['GET'])
@request_exception_handler
async def get_workloads():
    repo = get_workload_repo()
    saved_workloads = await repo.list_async()

    return [workload.to_dict() for workload in saved_workloads]


@app.route("/workloads/<workload_id>", methods=['GET'])
@request_exception_handler
def get_workload(workload_id):
    print(request)

    repo = get_workload_repo()
    workload = await repo.get_async(workload_id)

    return workload.to_dict()


@app.route("/workloads", methods=['POST'])
@request_exception_handler
def create_workload():
    print(request)

    workload_params = _parse_workload_params(request.get_json())
    workload_params.pop('id')

    workload = Workload(**workload_params)
    repo = get_workload_repo()

    workload_id = await repo.create_async(workload)

    return f"Workload was created successfully with id: {workload_id}"


@app.route("/workloads/<workload_id>", methods=['PUT'])
@request_exception_handler
def update_workload(workload_id):
    repo = get_workload_repo()
    workload_params = _parse_workload_params(request.get_json())
    workload = loop.run_until_complete(repo.get_async(workload_id))

    if workload_params['credentials']:
        workload.credentials = workload_params['credentials']
    if workload_params['mount_points']:
        workload.storage = workload_params['mount_points']

    loop.run_until_complete(repo.update_async(workload_id, workload))
    return "Workload was updated successfully"


@app.route("/workloads/<workload_id>", methods=['DELETE'])
@request_exception_handler
def delete_workload(workload_id):
    repo = get_workload_repo()

    loop.run_until_complete(repo.delete_async(workload_id))
    return "Workload was deleted successfully"


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


@app.route("/migrations", methods=['GET'])
@request_exception_handler
def get_migrations():
    repo = get_migration_repo()
    saved_migrations = loop.run_until_complete(repo.list_async())
    return [m.to_dict() for m in saved_migrations]


@app.route("/migrations/state/<migration_id>", methods=['GET'])
@request_exception_handler
def get_migration_state(migration_id):
    repo = get_migration_repo()
    migration = loop.run_until_complete(repo.get_async(migration_id))
    return migration.migration_state


def get_workload_repo():
    asyncio.set_event_loop(loop)
    client = MotorClientFactory.create_from_env()
    return WorkloadsRepo(client)


def get_migration_repo():
    asyncio.set_event_loop(loop)
    client = MotorClientFactory.create_from_env()
    return MigrationRepo(client)

