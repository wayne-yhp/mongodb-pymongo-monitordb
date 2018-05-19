import sys
import traceback
import pymongo


#初始化mongodb操作类
class DBInfo:
    def __init__(self, username, password, addr, db_name, collection_name, port):
        self.__username = username
        self.__password = password
        self.__addr = addr
        self.__db_name = db_name
        self.__collection_name = collection_name
        self.__port = port
        self.__db_collection = None
        self.__client = None
        self.__connect()


    #负责mongodb的连接
    def __connect(self):
        try:
            if self.__username is None and self.__password is None:
                client = pymongo.MongoClient('mongodb://' + self.__addr + ':' + self.__port + '/' + self.__db_name)
                db = client[self.__db_name]
            else:
                self.__client = pymongo.MongoClient('mongodb://' + self.__addr + ':' + self.__port + '/' + self.__db_name)
                db = self.__client[self.__db_name]
                db.authenticate(self.__username, self.__password)

            self.__db_collection = db[self.__collection_name]

        except :
            print('File  ' + __file__ + traceback.format_exc(1))
            self.close(client)
            sys.exit()

    #查询数据库指定集合的记录数量
    def count(self):
        return self.__db_collection.count()


    #数据库关闭
    def close(self):
        if self.__client is not None:
            self.__client.close()





