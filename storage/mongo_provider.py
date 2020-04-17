import motor.motor_asyncio


class MongoDbProvider:

    @classmethod
    def obtain_client(cls):
        username = "root"
        password = "password"
        eng = motor.motor_asyncio.AsyncIOMotorClient(
            'mongodb://{}:{}@{}:{}'.format(username, password, "centos7", 27017))

        return eng
