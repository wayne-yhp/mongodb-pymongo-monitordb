import getopt
import sys


#提示信息
def usage():
    print('\tCommand Options:')
    print('\t-u <username> with argument')
    print('\t-p <password> with argument')
    print('\t-i <ip_address> with argument')
    print('\t-d <database_name> with argument')
    print('\t-c <collection> with argument')
    print('\t-P <port> with argument')
    print('\t-h <help> \n')
    print('\tExamples:')
    print('\tpython main.py -u <username> -p <password> -i <ip_address> -d <database_name> -c <collection> -P <Port>')
    print('\tpython main.py -i <ip_address> -d <database_name> -c <collection>')
    print('\tpython main.py -h\n')
    print('\tAttention:')
    print('\t-h <help> can\'t be used together with other options')
    sys.exit()



#接收分析在终端调用时传来的参数
def receive_argument():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'u:p:i:d:c:P:h', ['username=', 'password=', 'ip_address=',
                                                                      'database_name=', 'collection=', 'port=', 'help'])
        if len(opts) < 3:
            usage()
    except getopt.GetoptError:
        print('\tERROR:incorrect argument')
        usage()

    addr = None
    db_name = None
    collection_name = None
    username = None
    password = None
    port = None

    for opt, arg in opts:
        if opt in('-u', '--username'):
            username = arg
        elif opt in('-p', '--password'):
            password = arg
        elif opt in('-i', '--ip_address'):
            addr = arg
        elif opt in('-d', '--database_name'):
            db_name = arg
        elif opt in('-c', '--collection'):
            collection_name = arg
        elif opt in ('-P', '--port'):
            port = arg
        elif opt in('-h', '--help'):
            usage()

    if username is None and password is not None:
        usage()
    elif username is not None and password is None:
        password = input('Please Enter Password:')

    #将分析好的参数返回用于数据库连接
    return [username, password, addr, db_name, collection_name, port]