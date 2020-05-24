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