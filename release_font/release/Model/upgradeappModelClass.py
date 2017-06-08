#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    任务模型获取 任务相关信息返回
'''

from django.db import connection

class upgradeappModelClass(object):


    ##  查询接口  ##
    def __cursorQuery(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
        except Exception,e:
            print "Catch exception : " + str(e)
        return cursor.fetchall()

    ## 通过包名查应用 ##
    def getnamebypkgname(self,pkgname):
        sql = """select name from upgrade_app where pkgname = %s"""
        data = self.__cursorQuery(sql,[pkgname])
        if len(data) != 0:
            return data[0][0]
        else:
            return ''

    def getipbyname(self,name,env_child):
        print name,env_child
        sql = """select t3.ip from upgrade_app t1,upgrade_app_machine t2,upgrade_machine t3,release_env_child t4
                  ,upgrade_env_machine t5 where t1.name=%s
              and t1.id=t2.app_id and t3.id=t2.machine_id and t4.envchild_name=%s and t4.id=t5.env_id and t3.id=t5.machine_id"""
        data = self.__cursorQuery(sql,[name,env_child])
        if len(data) != 0:
            return data
        else:
            return ''