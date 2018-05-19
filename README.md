# mongodb-pymongo-monitordb
该项目属运维工具，用于监测mongodb数据库数量变化，本人使用依赖如下：

- python2.7
- mongodb3.6
- 系统版本MAC OS X EI Captian
- 配置好python及mongodb环境变量

## 使用示例
> 先打开终端，启动mongodb服务(-auth:我的数据库开启了权限认证，需要输入账户密码，若没有，不写和不用输入账户密码，－dbpath:指定数据库的数据存储路径)

    mongod -auth -dbpath /Volumes/emergency2/mongodb-osx-x86_64-3.6.4/data

>打开另一个终端，进入到该项目路径下，用指令调用main主函数（指定ip,数据库名，集合名，端口号，用户名和密码可选）

    python3.6 main.py -u test1 -p test1 -i 127.0.0.1 -d test -c col -P 27017
    

每30秒会自动监测一次变化，并把数据写入count.txt中，数据库断线会自动重连
