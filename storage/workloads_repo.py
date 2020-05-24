from models.workload import Workload
from storage.cruid_repository import CruidRepository


class WorkloadsRepo(CruidRepository):

    def __init__(self, mongo_client):
        super().__init__(mongo_client, collection_name="workloads")

    def create_model_from_dict(self, d: dict, obj_id: str):
        d["id"] = obj_id
        return Workload(**d)
