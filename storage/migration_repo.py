from models.migration import Migration
from storage.cruid_repository import CruidRepository


class MigrationRepo(CruidRepository):

    def __init__(self, mongo_client):
        super().__init__(mongo_client, collection_name="models")

    def create_model_from_dict(self, d: dict, obj_id: str):
        d["id"] = obj_id
        return Migration(**d)
