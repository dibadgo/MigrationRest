import pickle
from bson import ObjectId


class MongoRepository:

    def __init__(self, mongo_client, collection_name):
        self.mongo_client = mongo_client
        self.collection_name = collection_name

    def _get_db(self):
        return self.mongo_client.mig_database

    def _get_collection(self):
        db = self._get_db()
        return db[self.collection_name]

    async def _save_document(self, document):
        document = self._encode(document)
        inserted_object = await self._get_collection().insert_one(document)

        return inserted_object

    async def _load_document(self, document_id):
        document = await self._get_collection().find_one({'_id': ObjectId(document_id)})
        if not document:
            raise RuntimeError('Document with id: {} does not exist!'
                               .format(document_id))

        return self._decode_document(document)

    async def _replace_document(self, document_id, document):
        collection = self._get_collection()

        result = await collection.replace_one({'_id': ObjectId(document_id)}, self._encode(document))
        return result

    @staticmethod
    def _encode(data):
        return {"data": pickle.dumps(data)}

    @staticmethod
    def _decode_document(document):
        return pickle.loads(document["data"])


class BaseRepository(MongoRepository):

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
        await collection.delete_many({'_id': document_id})
        print('%s documents after' % (await collection.count_documents({})))

