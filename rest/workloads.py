from typing import List

from fastapi import APIRouter, Depends

from binds.WorkloadBind import WorkloadBind
from models.workload import Workload
from rest.dependencies import repos_provider, RepoProvider


router = APIRouter()


@router.get("/workloads")
async def get_all(repos: RepoProvider = Depends(repos_provider)) -> List[Workload]:
    """ Returns all workloads

    :param repos: RepoProvider
    :return: List of workloads
    """
    wr = repos.workload_repo
    return [workload.to_dict() for workload in await wr.list_async()]


@router.get("/workloads/{workload_id}")
async def get_workload(workload_id, repos: RepoProvider = Depends(repos_provider)):
    """ Find the workload by Id

    :param workload_id: Workload id
    :param repos: RepoProvider
    :return: Workload
    """
    repo = repos.workload_repo
    workload = await repo.get_async(workload_id)

    return workload.to_dict()


@router.post("/workloads")
async def create_workload(bind: WorkloadBind, repos: RepoProvider = Depends(repos_provider)):
    """ Create the workload by provided configuration

    :param bind: Configuration
    :param repos: RepoProvider
    :return: Workload model
    """
    workload = bind.get_workload()

    repo = repos.workload_repo
    workload = await repo.create_async(workload)

    return workload.to_dict()


@router.patch("/workloads/{workload_id}")
async def update_workload(workload_id: str, bind: WorkloadBind, repos: RepoProvider = Depends(repos_provider)):
    """ Modify the workload by the provided configuration

    :param workload_id: Workload id
    :param bind: new configuration
    :param repos: RepoProvider
    :return: Updated workload model
    """
    repo = repos.workload_repo
    workload = await repo.get_async(workload_id)

    if bind.credentials:
        workload.credentials = bind.credentials
    if bind.storage:
        workload.storage = bind.storage

    updated_workload = await repo.update_async(workload_id, workload)
    return updated_workload


@router.delete("/workloads/{workload_id}")
async def delete_workload(workload_id, repos: RepoProvider = Depends(repos_provider)):
    """ Remove the workload model

    :param workload_id: Worklaod id
    :param repos: RepoProvider
    :return: Result message
    """
    repo = repos.workload_repo

    await repo.delete_async(workload_id)
    return "Workload was deleted successfully"
