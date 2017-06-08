#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    任务模型获取 任务相关信息返回
'''
from ..lib.pub import *

from django.db import connection

class upgradestepModeClass(object):


    ##  查询接口  ##
    def __cursorQuery(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
        except Exception,e:
            print "Catch exception : " + str(e)
        return cursor.fetchall()


    ## 通过步骤name查步骤id##

    def getidbyname(self,name):
        sql="""select id from upgrade_step where name=%s"""
        data=self.__cursorQuery(sql,[name])
        return data[0]

    ## 通过步骤id查步骤name#

    def getnamebyid(self,id):
        sql="""select name from upgrade_step where id=%s"""
        data=self.__cursorQuery(sql,[id])
        return data[0][0]

    def getremark(self,id):
        sql="""select remark from upgrade_step where id=%s"""

        data=self.__cursorQuery(sql,[id])
        return data[0][0]