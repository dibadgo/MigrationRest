from storage.repository import Repository


class WorkloadsRepo(Repository):

    def __init__(self, mongo_client):
        super().__init__(mongo_client, "workloads")

    async def create_workload_async(self, workload):
        workload_id = await self._save_document(workload)

        print(workload_id.inserted_id)
        return workload_id.inserted_id

    async def get_workload_async(self, workload_id):
        workload = await self._load_document(workload_id)
        return workload

    async def get_workloads_async(self):
        collection = self._get_collection()

        workloads = []
        async for workload in collection.find({}):
            workloads += [self._decode_document(workload)]

        return workloads

    async def update_workload_async(self, workload_id, workload):
        old_document = await self._load_document(workload_id)
        print('found workload: {}'.format(old_document))

        result = await self._replace_document(workload_id, workload)
        print('replaced {} document'.format(result.modified_count))

    async def delete_workload_async(self, workload_id):
        collection = self._get_collection()

        n = await collection.count_documents({})

        print('%s documents before calling delete_many()' % n)
        await collection.delete_many({'_id': workload_id})
        print('%s documents after' % (await collection.count_documents({})))