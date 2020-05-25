import logging
from bson import ObjectId
from storage.mongo_repository import MongoRepository


class CruidRepository(MongoRepository):
    """The abstract repository implemented all CRUID operations"""

    def __init__(self, mongo_client, collection_name):
        """ C-tor

        :param mongo_client: Mongo (motor) client
        :param collection_name: Database(collection) name
        """
        super().__init__(mongo_client, collection_name)

    async def create_async(self, document):
        """ Create a document

        :param document: document to insert
        :return: Created document
        """
        inserted = await self._save_document(document)

        logging.debug(f"Inserted document {inserted.inserted_id}")

        return await self.get_async(inserted.inserted_id)

    async def get_async(self, document_id):
        """ Find the Document by Id

        :param document_id: documentId
        :return: Document
        """
        migration = await self._load_document(document_id)
        return migration

    async def list_async(self):
        """ Get all document from a collection

        :return: List of documents
        """
        collection = self._get_collection()

        documents = []
        async for document in collection.find({}):
            documents += [self._decode_document(document)]

        return documents

    async def update_async(self, document_id, document):
        """ Update the document by id

        :param document_id: document id
        :param document: New document
        :return: Updated document
        """
        old_document = await self._load_document(document_id)
        logging.debug(f"Found workload {old_document}")

        result = await self._replace_document(document_id, document)
        logging.debug(f'Replaced {result.modified_count} document')

        return await self.get_async(document_id)

    async def delete_async(self, document_id):
        """ Remove the document from Db

        :param document_id: Document id
        :return: Number of removed documents
        """
        collection = self._get_collection()

        n = await collection.count_documents({})

        logging.debug('%s documents before calling delete_many()' % n)
        await collection.delete_many({'_id': ObjectId(document_id)})

        total_documents = await collection.count_documents({})
        logging.debug('%s documents after' % total_documents)

        return n - total_documents

