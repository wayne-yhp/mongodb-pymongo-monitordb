# -*- coding: UTF-8 -*-
from dbmonitor import count_record
from Utils import convert_utils



if __name__ == '__main__':

    info_list = convert_utils.receive_argument()
    count_record.monitor_mongo(info_list[0], info_list[1], info_list[2], info_list[3], info_list[4], info_list[5])
