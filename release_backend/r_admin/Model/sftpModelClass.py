#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    sftp 模型获取，数据接口
'''

from django.db import connection

class SftpModelClass(object):

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

    # 根据 project_id / env_id 确定是否需要插入中间表，如果没有值，则需要插入
    def getInsertToProjectEnvId(self, project_id, env_id):
        sql = '''select id from release_project_env_child where project_id=%s and env_child_id=%s'''
        data = self.__cursorQuery(sql, [project_id, env_id])
        try:
            return data[0][0]
        except:
            return ''

    # 判断是否有重复的item 在project_env_id 相同的情况下
    def isDuplicateData(self, item_name, project_env_id):
        sql = '''select id from release_config where item=%s and project_env_id=%s'''
        data = self.__cursorQuery(sql, [item_name, project_env_id])
        print 'data11111111:xx',data
        try:
            return data[0][0]
        except:
            return ''

    # 添加数据到项目 环境中间表中
    def addProjectEnv(self, project_id, env_id):
        sql = '''insert into release_project_env_child(project_id,env_child_id) values (%s,%s)'''
        return self.__cursorInsert(sql, [project_id, env_id])

    # 添加数据到配置表中
    def addConfig(self, data, project_env_id):     # project_env_id 为 项目环境中间表id
        sql = '''insert into release_config(item,value,remark,project_env_id) values (%s,%s,%s,%s)'''
        return self.__cursorInsert(sql, [data['item'], data['value'], data['remark'], project_env_id])


    # sftp 列表信息
    def sftpList(self):
        sql = '''select t1.id,
                        t1.item,
                        t1.value,
                        t1.remark,
                        t3.name as project_code,
                        t3.remark as project_remark,
                        t4.envchild_name as env_name,
                        t3.id as project_id,
                        t4.id as env_id
                 from release_config t1, release_project_env_child t2, release_project t3, release_env_child t4
                 where t1.project_env_id = t2.id and
                       t2.project_id = t3.id and
                       t2.env_child_id = t4.id
              '''
        return  self.__cursorQuery(sql, [])

    # 删除 环境信息
    def deleteSftp(self, id):
        sql = '''select project_env_id from release_config where id=%s'''  # 通过id 获取到 project_env_id
        data = self.__cursorQuery(sql,[id])
        try:
            project_env_id = data[0][0]
        except:
            print '== [ERROR] not find project_env_id ==='
            return ''
        sql2 = '''select count(*) from release_config where project_env_id=%s'''
        data2 = self.__cursorQuery(sql2, [project_env_id])
        try:
            count = data2[0][0]
        except:
            print '== [ERROR] not find project_env_id 2 ==='
            return ''
        sql_del1 = '''delete from release_config where id=%s'''
        if int(count) >= 1:
            return self.__cursorInsert(sql_del1, [id])  # 删除单行数据
        else:
            d_id = self.__cursorInsert(sql_del1, [id])  # 删除单行数据
            if d_id != '':
                sql_del2 = '''delete from release_project_env_child where id=%s'''  # 删除中间表
                return self.__cursorInsert(sql_del2, [data[0][0]])
            else:
                return ''








#########################################