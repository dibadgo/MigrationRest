import asyncio

from fastapi import APIRouter

from binds.WorkloadBind import WorkloadBind
from main import app
from rest.handlers import request_exception_handler
from storage.migration_repo import MigrationRepo
from storage.mongo_provider import MotorClientFactory
from models.mount_point import MountPoint
from models.credentials import Credentials
from models.workload import Workload
from storage.workloads_repo import WorkloadsRepo


router = APIRouter()

#
# @router.post("/workloads22", tags=["workloads22"])
# def test_method(workload: WorkloadBind):
#     print(workload)
#
#     return MountPoint("ololo", 123)


@router.get("/workloads")
async def get_all():
    repo = _get_workload_repo()
    saved_workloads = await repo.list_async()

    return [workload.to_dict() for workload in saved_workloads] # TODO try with yield from


@router.get("/workloads/{workload_id}")
async def get_workload(workload_id):
    repo = _get_workload_repo()
    workload = await repo.get_async(workload_id)

    return workload.to_dict()


@router.post("/workloads")
async def create_workload(workload: Workload):
    # workload: WorkloadBind
    # workload = Workload(**workload_params)
    repo = _get_workload_repo()

    workload_id = await repo.create_async(workload)

    return f"Workload was created successfully with id: {workload_id}"


@router.put("/workloads/{workload_id>}")
async def update_workload(workload_id: str, bind: WorkloadBind):
    repo = _get_workload_repo()
    workload_params = _parse_workload_params(request.get_json())
    workload = loop.run_until_complete(repo.get_async(workload_id))

    if workload_params['credentials']:
        workload.credentials = workload_params['credentials']
    if workload_params['mount_points']:
        workload.storage = workload_params['mount_points']

    await repo.update_async(workload_id, workload)
    return "Workload was updated successfully"


@router.delete("/workloads/{workload_id>}")
async def delete_workload(workload_id):
    repo = _get_workload_repo()

    await repo.delete_async(workload_id)
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


def _get_workload_repo():
    client = MotorClientFactory.create_from_env()
    return WorkloadsRepo(client)
