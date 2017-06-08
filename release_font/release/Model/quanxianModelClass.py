#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    任务模型获取 任务相关信息返回
'''
from ..lib.pub import *

from django.db import connection

class quanxianModelClass(object):


    ##  查询接口  ##
    def __cursorQuery(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
        except Exception,e:
            print "Catch exception : " + str(e)
        return cursor.fetchall()

    ##  插入接口  ##
    def __cursorInsert(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
            return int(cursor.lastrowid)
        except Exception,e:
            print "Catch exception : " + str(e)
            return ''

    def __cursorUpdate(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
            return int(cursor.lastrowid)
        except Exception, e:
            print "Catch exception : " + str(e)
            return ''


    def getenvnamebyuser(self,username):
        sql = """select t4.envchild_name from auth_user t1,auth_user_groups t2,release_group_env_child t3 ,release_env_child t4
where t1.id=t2.user_id and t3.gid=t2.group_id and t4.id=t3.env_child_id and t1.username=%s"""
        data = self.__cursorQuery(sql, [username])
        retlist=[]
        if len(data) != 0:
            for item in data:
                retlist.append(item[0])
            return retlist
        else:
            return ''



#########################################
# if __name__=='__main__':
#     tscl=TaskModelClass()
#     tscl.getAppNameByWarName('beehive.war')
