#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    机器模型获取，数据接口
'''

from django.db import connection

class EnvModelClass(object):

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

    # 获取 所有环境信息 [('1', 'sit1'), ('2', 'sit2')]
    def getEnvInfo(self):
        sql = '''select id,envchild_name from release_env_child'''
        data = self.__cursorQuery(sql,[])
        return data

    def getEnvInfo2(self):
        sql = '''select id,envchild_name,env_id_id from release_env_child'''
        data = self.__cursorQuery(sql,[])
        return data

    # 插入机器环境对应信息 到中间表
    def addDataEnvMachine(self, lst):
        sql = '''insert into upgrade_env_machine(machine_id,env_id) values (%s,%s)'''
        return self.__cursorInsert(sql, [lst[0], lst[1]])

    # 添加 环境信息
    def addEnv(self, name, env_id):
        sql = '''insert into release_env_child(envchild_name,env_id_id) values (%s,%s)'''
        return self.__cursorInsert(sql, [name, env_id])

    # 删除 环境信息
    def deleteEnv(self, id):
        sql = '''delete from release_env_child where id=%s'''
        return self.__cursorInsert(sql, [id])

    # 更新 机器环境对应信息 到中间表
    def updateDataEnvMachine(self, machine_id, env_id):
        sql = '''update upgrade_env_machine
                 set env_id=%s
                 where machine_id=%s
              '''
        try:
            data = self.__cursorInsert(sql, [env_id, machine_id])
            return True
        except:
            return False


    # 通过 env id 获取 相关信息
    def getEnvInfoById(self, id):
        sql = '''select t1.id,
                        t1.envchild_name as env_name,
                        t2.name as env_step,
                        t2.id as step_id
                 from release_env_child t1, release_env t2
                 where t1.env_id_id=t2.id and t1.id=%s
              '''
        data = self.__cursorQuery(sql, [id])
        return data


    # 更新 环境信息 数据接口
    def updateEnv(self, data):
        sql = '''update release_env_child set envchild_name=%s,env_id_id=%s where id=%s'''
        try:
            self.__cursorInsert(sql, [data['name'], data['step_id'], data['id']])
            return data['id']
        except:
            return ''







#########################################