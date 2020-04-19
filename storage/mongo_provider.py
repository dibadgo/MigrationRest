import motor.motor_asyncio


class MongoDbProvider:

    @classmethod
    def obtain_client(cls):
        username = "root"
        password = "password"
        host = "centos7"
        port = 27017

        conn_string = 'mongodb://{usr}:{passwd}@{host}:{port}'.format(
            usr=username, passwd=password, host=host, port=port)
        return motor.motor_asyncio.AsyncIOMotorClient(conn_string)
