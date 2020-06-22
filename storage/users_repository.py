import hashlib
from typing import Optional

from models.user import UserInDB, User
from storage.mongo_repository import MongoRepository


class UsersRepo(MongoRepository):
    """The concrete implementation of Users repo"""

    def __init__(self, mongo_client):
        super().__init__(mongo_client, collection_name="users")

    def create_model_from_dict(self, d: dict, obj_id: str) -> UserInDB:
        d["id"] = obj_id
        return UserInDB(**d)

    async def get_user(self, name: str) -> Optional[UserInDB]:
        """ Provide the user by username

        :param name: username
        :return: User
        """
        document = await self._get_collection().find_one({'data.username': name})
        if not document:
            return None

        return self._decode_document(document)

    async def create_user(self, user: User, password: str) -> UserInDB:
        """ Save a new user to the DB

        :param user: User
        :param password: User password
        :return: User
        """
        if await self.get_user(user.username):
            raise RuntimeError(f'User with name: {user.username} already exist!')

        hashed_password = self._hash_password(password)
        db_user = self._create_user_db(user, hashed_password)

        created_user = await self._save_document(db_user)

        return await self._load_document(created_user.inserted_id)

    async def check_password(self, user: UserInDB, password: str) -> bool:
        """ Check the password hash

        :param user: UserInDB
        :param password: original password
        :return: True if the passwords match
        """
        return user.hashed_password == self._hash_password(password)

    @staticmethod
    def _hash_password(password: str) -> str:
        """ Takes a hash sum from the password string

        :param password: User's password
        :return: Hashed string
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def _create_user_db(user: User, hashed_password: str) -> UserInDB:
        """ Create a user model to save in DB

        :param user: User
        :param hashed_password: hashed password
        :return: UserInDB
        """
        return UserInDB(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=user.disabled,
            hashed_password=hashed_password
        )
