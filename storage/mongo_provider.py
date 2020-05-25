import logging
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
        username = environ.get("MM_MONGO_USR")
        password = environ.get("MM_MONGO_PASS")
        host = environ.get("MM_MONGO_HOST")
        port = environ.get("MM_MONGO_PORT")

        connection_string = f'mongodb://{username}:{password}@{host}:{port}'
        logging.debug(f"Mongo connection string {connection_string}")

        return AsyncIOMotorClient(f'mongodb://{username}:{password}@{host}:{port}')
