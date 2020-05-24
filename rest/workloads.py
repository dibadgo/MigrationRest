from typing import List

from fastapi import APIRouter

from binds.WorkloadBind import WorkloadBind
from models.workload import Workload
from storage.mongo_provider import MotorClientFactory
from storage.workloads_repo import WorkloadsRepo


router = APIRouter()


@router.get("/workloads")
async def get_all() -> List[Workload]:
    """ Returns all workloads

    :return: List of workloads
    """
    repo = _get_workload_repo()

    return [workload.to_dict() for workload in await repo.list_async()]


@router.get("/workloads/{workload_id}")
async def get_workload(workload_id):
    """ Find the workload by Id

    :param workload_id: Workload id
    :return: Workload
    """
    repo = _get_workload_repo()
    workload = await repo.get_async(workload_id)

    return workload.to_dict()


@router.post("/workloads")
async def create_workload(bind: WorkloadBind):
    """ Create the workload by provided configuration

    :param bind: Configuration
    :return: Workload model
    """
    workload = bind.get_workload()

    repo = _get_workload_repo()
    workload = await repo.create_async(workload)

    return workload.to_dict()


@router.patch("/workloads/{workload_id}")
async def update_workload(workload_id: str, bind: WorkloadBind):
    """ Modify the workload by the provided configuration

    :param workload_id: Workload id
    :param bind: new configuration
    :return: Updated workload model
    """
    repo = _get_workload_repo()
    workload = await repo.get_async(workload_id)

    if bind.credentials:
        workload.credentials = bind.credentials
    if bind.storage:
        workload.storage = bind.storage

    updated_workload = await repo.update_async(workload_id, workload)
    return updated_workload


@router.delete("/workloads/{workload_id}")
async def delete_workload(workload_id):
    """ Remove the workload model

    :param workload_id: Worklaod id
    :return: Result message
    """
    repo = _get_workload_repo()

    await repo.delete_async(workload_id)
    return "Workload was deleted successfully"


def _get_workload_repo():
    client = MotorClientFactory.create_from_env()
    return WorkloadsRepo(client)
