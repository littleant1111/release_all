#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    项目模型获取 项目相关信息返回
'''

from django.db import connection

class ProjectModelClass(object):

    ##  查询接口  ##
    def __cursorQuery(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
        except Exception,e:
            print "Catch exception : " + str(e)
        return cursor.fetchall()

    #### 根据项目id获取对应的 应用名称  用列表返回  #####
    def getAppNameByProjectId(self, project_id):
        ret_list = []
        sql = 'select a.name from upgrade_app a,release_project p \
               where a.project_id = p.id and p.id = %s'
        data = self.__cursorQuery(sql, [project_id])
        if data is None:
            return ''
        else:
            for i in range(len(data)):
                ret_list.append(data[i][0])
        # print "data,,, is ", data
        return ret_list

    #### 根据项目编码 获取对应的 应用名称  用列表返回  #####
    def getAppNameByProjectNo(self, project_no):
        ret_list = []
        sql = '''select a.name from upgrade_app a,release_project p
                    where a.project_id=p.id and p.name=%s'''
        data = self.__cursorQuery(sql, [project_no])
        if data is None:
            return ''
        for i in range(len(data)):
            appname = data[i][0]
            if appname not in ret_list:
                ret_list.append(data[i][0])
        return ret_list

    # 返回项目的id 、名称 [[1,'HCS'], [2, 'ALS'], []]
    def getProjectInfo(self):
        sql = 'select id,name \
               from release_project'
        data = self.__cursorQuery(sql, [])
        print "data0000:,x:",data
        return data

    ## 通过war包名查appname ##
    def getAppNameBywar(self, pkg_name):
        ret_list = []
        sql = '''select DISTINCT(name) from upgrade_app where  pkgname=%s'''
        data = self.__cursorQuery(sql, [pkg_name])
        if data is None:
            return ''
        return data[0][0]
    # 根据项目名获取项目 id
    def getProjectIdByName(self, name):
        pass



#########################################