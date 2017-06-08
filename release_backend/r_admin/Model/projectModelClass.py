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

    ##  插入接口  ##
    def __cursorInsert(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
            return int(cursor.lastrowid)
        except Exception, e:
            print "Catch exception : " + str(e)
            return ''

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


    # 添加项目数据接口
    def addProject(self, data):
        sql = '''insert into release_project(name,remark) values (%s, %s)'''
        return self.__cursorInsert(sql, [data['name'], data['remark']])

    # 添加项目环境中间表数据
    def addProjectEnv(self, id, lst):
        for i in range(len(lst)):
            sql = '''insert into release_project_env_child(project_id,env_child_id) values (%s,%s)'''
            rid = self.__cursorInsert(sql, [id, lst[i]])
            if rid == '':
                return ''
        return '1'

    #获取项目信息 所有 [['1', 'HCS', '蜂巢系统'], ['1', 'ALS', '安硕核心']]
    def getProjectInfo2(self):
        sql = 'select id,name,remark \
                       from release_project'
        data = self.__cursorQuery(sql, [])
        return data

    # 删除对应的项目
    def deleteProject(self, id):
        sql = '''delete from release_project where id=%s'''
        return self.__cursorInsert(sql, [id])

    # 删除 项目环境 中间表数据
    def deleteProjectEnv(self, project_id):
        sql = '''delete from release_project_env_child where project_id=%s'''
        return self.__cursorInsert(sql, [project_id])

    ## 检测项目编码是否存在
    def checkProjectCode(self, code):
        sql = '''select id from release_project where name=%s'''
        data = self.__cursorQuery(sql, [code])
        try:
            rid = data[0][0]
            return rid
        except:
            return ''

    # 通过 project_id 获取项目信息 所有 [['1', 'HCS', '蜂巢系统'], ['1', 'ALS', '安硕核心']]
    def getProjectInfoById(self, id):
        sql = '''select t1.id,
                        t1.name,
                        t1.remark
                 from release_project t1
                 where t1.id=%s
              '''
        data = self.__cursorQuery(sql, [id])
        return data

    # 根据 project id 获取 [('id', 'envchild_nam', 'env_id'), ('1', 'sit1', '1')]
    def getProjectEnvInfoById(self, id):
        sql = '''select t1.id,
                        t1.name,
                        t1.remark ,
                        t3.envchild_name,
                        t3.id as env_id
                 from release_project t1, release_project_env_child t2, release_env_child t3
                 where t1.id=t2.project_id and t2.env_child_id=t3.id and t1.id=%s
              '''
        data = self.__cursorQuery(sql, [id])
        # print '8888888888888:',data
        try:
            return data
        except:
            return ''

    # 更新 项目数据接口
    def updateProject(self, data):
        sql = '''update release_project set name=%s,remark=%s where id=%s'''
        return self.__cursorInsert(sql, [data['name'], data['remark'], data['id']])

    # 更新 项目环境中间表数据
    def updateProjectEnv(self, id, lst):
        did = self.deleteProjectEnv(id)
        if did != '':
            return self.addProjectEnv(id, lst)
            # for i in range(len(lst)):
            #     sql = '''update release_project_env_child set env_child_id=%s where project_id=%s'''
            #     rid = self.__cursorInsert(sql, [id, lst[i]])
            #     if rid == '':
            #         return ''
            # return '1'
        else:
            return ''



#########################################