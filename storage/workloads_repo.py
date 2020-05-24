from storage.cruid_repository import CruidRepository


class WorkloadsRepo(CruidRepository):

    def __init__(self, mongo_client):
        super().__init__(mongo_client, collection_name="workloads")
