from storage.baserepository import BaseRepository


class MigrationRepo(BaseRepository):

    def __init__(self, mongo_client):
        super().__init__(mongo_client, "migrations")
