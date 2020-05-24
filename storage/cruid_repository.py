from bson import ObjectId

from storage.mongo_repository import MongoRepository


class CruidRepository(MongoRepository):

    def __init__(self, mongo_client, collection_name):
        super().__init__(mongo_client, collection_name)

    async def create_async(self, document):
        inserted = await self._save_document(document)

        print(inserted.inserted_id)
        return inserted.inserted_id

    async def get_async(self, document_id):
        migration = await self._load_document(document_id)
        return migration

    async def list_async(self):
        collection = self._get_collection()

        documents = []
        async for document in collection.find({}):
            documents += [self._decode_document(document)]

        return documents

    async def update_async(self, document_id, document):
        old_document = await self._load_document(document_id)
        print('found workload: {}'.format(old_document))

        result = await self._replace_document(document_id, document)
        print('replaced {} document'.format(result.modified_count))

    async def delete_async(self, document_id):
        collection = self._get_collection()

        n = await collection.count_documents({})

        print('%s documents before calling delete_many()' % n)
        await collection.delete_many({'_id': ObjectId(document_id)})

        total_documents = await collection.count_documents({})
        print('%s documents after' % total_documents)

        return n - total_documents

