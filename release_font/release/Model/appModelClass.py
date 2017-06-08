#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import connection

class AppModelClass(object):

    ##  查询接口  ##
    def __cursorQuery(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
        except Exception,e:
            print "Catch exception : " + str(e)
        return cursor.fetchall()

    #### 根据包名 获取应用的名称  #####
    def getAppNameByWarName(self, warname):
        sql = 'select name from upgrade_app \
                where pkgname=%s \
                limit 1'
        data = self.__cursorQuery(sql, [warname])
        if len(data)!=0:
            appname = data[0][0]
            # print "3333333333 value,",value
            return appname
        else:
            return ''

    #### 根据app ip 获取应用连接信息  #####
    def getuserByappip(self, app,ip):
        sql = """select t4.name,t4.`password`,t3.ip,t4.sshport from upgrade_app t1, upgrade_app_machine t2,upgrade_machine t3,upgrade_user t4
where t1.id=t2.app_id and t2.machine_id=t3.id and  t4.machine_id=t3.id and t4.`name`=t1.`user` and t1.`name`=%s
and t3.ip=%s"""
        data = self.__cursorQuery(sql, [app,ip])
        dic = {}

        if len(data) != 0:
            dic['username'] = data[0][0]
            dic['password'] = data[0][1]
            dic['ip'] = data[0][2]
            dic['port'] = data[0][3]
            # print "3333333333 value,",value
            return dic
        else:
            return dic

#########################################