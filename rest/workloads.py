from typing import List

from fastapi import APIRouter

from binds.WorkloadBind import WorkloadBind
from models.workload import Workload
from storage.mongo_provider import MotorClientFactory
from storage.workloads_repo import WorkloadsRepo


router = APIRouter()


@router.get("/workloads")
async def get_all() -> List[Workload]:
    repo = _get_workload_repo()

    return [workload.to_dict() for workload in await repo.list_async()]


@router.get("/workloads/{workload_id}")
async def get_workload(workload_id):
    repo = _get_workload_repo()
    workload = await repo.get_async(workload_id)

    return workload.to_dict()


@router.post("/workloads")
async def create_workload(bind: WorkloadBind):
    workload = bind.get_workload()

    repo = _get_workload_repo()
    workload_id = await repo.create_async(workload)

    return f"Workload was created successfully with id: {workload_id}"


@router.patch("/workloads/{workload_id}")
async def update_workload(workload_id: str, bind: WorkloadBind):
    repo = _get_workload_repo()
    workload = await repo.get_async(workload_id)

    if bind.credentials:
        workload.credentials = bind.credentials
    if bind.storage:
        workload.storage = bind.storage

    await repo.update_async(workload_id, workload)
    return "Workload was updated successfully"


@router.delete("/workloads/{workload_id}")
async def delete_workload(workload_id):
    repo = _get_workload_repo()

    await repo.delete_async(workload_id)
    return "Workload was deleted successfully"


def _get_workload_repo():
    client = MotorClientFactory.create_from_env()
    return WorkloadsRepo(client)
