import pickle

from bson import ObjectId
from pydantic import BaseModel


class MongoRepository:
    """Abstract Mongo repository which wraps the required operations"""

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
            raise RuntimeError(f'Document with id: {document_id} does not exist!')

        return self._decode_document(document)

    async def _replace_document(self, document_id, document):
        collection = self._get_collection()

        result = await collection.replace_one({'_id': ObjectId(document_id)}, self._encode(document))
        return result

    def _encode(self, data: BaseModel):
        return {"data": self.model_to_dict(data)}

    def _decode_document(self, document):
        return self.create_model_from_dict(document["data"], str(document["_id"]))

    def model_to_dict(self, model: BaseModel) -> dict:
        return model.dict()

    def create_model_from_dict(self, d: dict, obj_id: str):
        pass
