#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    机器模型获取，数据接口
'''

from django.db import connection

class MachineModelClass(object):

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

    # 添加机器信息
    def addMachineInfo(self, data):
        sql = '''insert into upgrade_machine(name,hostname,ip,is_vm,cpuinfo,memoryinfo) values (%s,%s,%s,%s,%s,%s)'''
        return self.__cursorInsert(sql,[data['name'], data['hostname'], data['ip'],data['is_vm'],data['cpuinfo'], data['memoryinfo']])


    # 获取机器 简要显示 信息
    def getMachineSimpleListInfo(self):
        sql = '''select id,name,hostname,ip from upgrade_machine'''
        return self.__cursorQuery(sql,[])

    # 获取机器列表信息
    def getMachineListInfo(self):
        sql = '''select id,name,hostname,ip,is_vm,cpuinfo,memoryinfo from upgrade_machine'''
        return self.__cursorQuery(sql,[])

    # 删除机器 数据接口
    def deleteMachine(self, id):
        sql = '''delete from upgrade_machine where id=%s'''
        return self.__cursorInsert(sql, [id])
        pass

    # 删除 环境 机器中间表
    def deleteEnvMachine(self, machine_id):
        sql = '''delete from upgrade_env_machine where machine_id=%s'''
        return self.__cursorInsert(sql,[machine_id])

    # 检测ip 是否在 machine 表中存在
    def checkip(self, ip):
        sql = '''select id from upgrade_machine where ip=%s'''
        data = self.__cursorQuery(sql, [ip])
        try:
            rid = data[0][0]
            return rid
        except:
            return ''

    # 根据id 获取 对应机器信息
    def getMachineInfoById(self, id):
        sql = '''select t1.id,
                 t1.name,
                 t1.hostname,
                 t1.ip,
                 t1.is_vm,
                 t1.cpuinfo,
                 t1.memoryinfo,
                 t3.id as env_id
                 from upgrade_machine t1, upgrade_env_machine t2, release_env_child t3
                 where t1.id=%s and t1.id=t2.machine_id and t2.env_id=t3.id
              '''
        data = self.__cursorQuery(sql, [id])
        dic = {}
        try:
            dic['id'] =   data[0][0]
            dic['name'] = data[0][1]
            dic['hostname'] = data[0][2]
            dic['ip'] = data[0][3]
            dic['is_vm'] = data[0][4]
            dic['cpuinfo'] = data[0][5]
            dic['memoryinfo'] = data[0][6]
            dic['env_id'] = data[0][7]
            return dic
        except:
            return ''

    # 更新 machine 信息
    def updateMachine(self, data):
        sql = '''update upgrade_machine
                 set name=%s,
                 hostname=%s,
                 ip=%s,
                 is_vm=%s,
                 cpuinfo=%s,
                 memoryinfo=%s
                 where id=%s
              '''
        try:
            data =  self.__cursorQuery(sql, [data['name'], data['hostname'], data['ip'], data['is_vm'], data['cpuinfo'], data['memoryinfo'], data['id']])
            return True
        except:
            return False



#########################################