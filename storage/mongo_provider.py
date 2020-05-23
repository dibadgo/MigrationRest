from os import environ
from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient


@dataclass
class MotorClientFactory:
    """Class for configure Motor client for MongoDb"""

    @classmethod
    def create_from_env(cls) -> AsyncIOMotorClient:
        username = environ.get("MM_MONGO_USR") or "root"
        password = environ.get("MM_MONGO_PASS") or "password"
        host = environ.get("MM_MONGO_HOST") or "centos7"
        port = environ.get("MM_MONGO_PORT") or 27017

        return AsyncIOMotorClient(f'mongodb://{username}:{password}@{host}:{port}')
