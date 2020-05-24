from os import environ
from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient


@dataclass
class MotorClientFactory:
    """Class for configure Motor client for MongoDb"""

    @classmethod
    def create_from_env(cls) -> AsyncIOMotorClient:
        """ Configure the Motor client for MongoDb from the environment variables

        :return: Motor client
        """
        username = environ.get("MM_MONGO_USR", "root")
        password = environ.get("MM_MONGO_PASS", "password")
        host = environ.get("MM_MONGO_HOST", "centos7")
        port = environ.get("MM_MONGO_PORT", 27017)

        return AsyncIOMotorClient(f'mongodb://{username}:{password}@{host}:{port}')
