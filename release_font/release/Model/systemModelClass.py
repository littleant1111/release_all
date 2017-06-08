#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import connection

class systemModelClass(object):

    ##  查询接口  ##
    def __cursorQuery(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
        except Exception,e:
            print "Catch exception : " + str(e)
        return cursor.fetchall()

    #### 查询日志的查询间隔  #####
    def getLogInterval(self):
        sql = 'select log_interval from check_system_parameter limit 1'
        data = self.__cursorQuery(sql, [])
        return data[0][0]

    #### 查询到日志的最后查询行数  #####
    def getLogTail(self):
        sql = 'select log_tail_line from check_system_parameter limit 1'
        data = self.__cursorQuery(sql, [])
        return data[0][0]

    #### 设置日志的刷新间隔和尾行数  #####
    def setLogParameters(self, interval, tail_line):
        sql = 'update check_system_parameter p set p.log_interval=%s, p.log_tail_line=%s where p.id=1'
        data = self.__cursorQuery(sql, [interval, tail_line])
        return '1'

    #### 得到日志的查询间隔和日志的每次查询行数 #########
    def getLogSettingInfo(self):
        sql = 'select log_interval,log_tail_line from check_system_parameter limit 1'
        data = self.__cursorQuery(sql, [])
        ret_dic = {}
        ret_dic['interval'] = data[0][0]
        ret_dic['log_tail_line'] = data[0][1]
        return ret_dic

#########################################