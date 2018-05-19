from dboperate import db_info
import os
import traceback
import time


#mongodb连接断线重连
def reconnect(username, password, addr, db_name, collection_name, port):
    traceback.format_exc(1)
    monitor_mongo(username, password, addr, db_name, collection_name, port)


#将查询结果写入count.txt文件下
def writecount(count):
    with open(os.getcwd() + os.sep + 'count.txt', 'w+') as f:
        f.write(count)


#每30s查询一次，对数据库进行数据量变化监测
def monitor_mongo(username, password, addr, db_name, collection_name, port):
    db_class = db_info.DBInfo(username, password, addr, db_name, collection_name, port)
    running = True
    while running:
        time.sleep(30)
        try:
            writecount(str(db_class.count()))
        except:
            db_class.close()
            reconnect(username, password, addr, db_name, collection_name, port)







