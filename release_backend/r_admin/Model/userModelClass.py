#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    用户模型获取
'''

from django.db import connection
from ..lib.pub import *

class UserModelClass(object):

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

    # 添加 用户 数据接口
    def addUser(self, data):
        sql = '''insert into upgrade_user(name, password, home_dir, machine_id, sshport)
                 values (%s, %s, %s, %s, %s)
        '''
        print 'adduser',data
        return self.__cursorInsert(sql, [data['name'], data['password'], data['home_dir'], data['machine_id'], data['sshport']])

    # 获取用户列表数据
    def getUserList(self):
        sql = '''select t1.id,
                        t1.name,
                        t1.home_dir,
                        t2.hostname,
                        t2.ip,
                        t1.sshport,
                        t1.machine_id,
                        t1.isconnected,
                        t1.connect_time
                 from upgrade_user t1, upgrade_machine t2
                 where t1.machine_id = t2.id
              '''
        retdata = []
        try:
            data = self.__cursorQuery(sql, [])
            # print '999999999999data:',data
            # print 'data[0][3]', data[0][3]
            for i in range(len(data)):
                dic = {}
                dic['id'] = data[i][0]
                dic['user'] = data[i][1]
                dic['home_dir'] = data[i][2]
                dic['hostname'] = data[i][3]
                dic['ip'] = data[i][4]
                dic['sshport'] = data[i][5]
                dic['machine_id'] = data[i][6]
                dic['isconnected'] = data[i][7]
                dic['connect_time'] = unixToDateTime(data[i][8])
                retdata.append(dic)
            # print 'retdata:',retdata
            return retdata
        except:
            return ''


    # 检测用户在主机上是否已经存在
    def checkUserMachineExists(self, user, machine_id):
        sql = '''select id from upgrade_user where name=%s and machine_id=%s'''
        data = self.__cursorQuery(sql, [user, machine_id])
        try:
            rid = data[0][0]
            if rid != '':
                return True
            else:
                return False
        except:
            return False

    # 删除用户
    def deleteUser(self, id):
        sql = '''delete from upgrade_user where id=%s'''
        return self.__cursorInsert(sql, [id])


    # 根据用户id 获取用户信息
    def getUserInfoById(self, id):
        sql = '''select t1.id,
                        t1.name,
                        t1.password,
                        t1.home_dir,
                        t1.machine_id,
                        t1.sshport
                 from upgrade_user t1
                 where t1.id=%s
              '''
        try:
            return self.__cursorQuery(sql, [id])
        except:
            return ''


    # 保存用户 接口
    def updateUser(self, data):
        sql = '''update upgrade_user set name=%s,password=%s,home_dir=%s,machine_id=%s,sshport=%s where id=%s'''
        try:
            self.__cursorQuery(sql, [data['name'],
                                    data['password'],
                                    data['home_dir'],
                                    data['machine_id'],
                                    data['sshport'],
                                    data['id']])
            return '1'
        except:
            return ''


    # 根据用户id 获取对应机器联系信息
    def getConnectInfo(self, id):
        sql = '''select t1.name,
                        t1.password,
                        t1.sshport,
                        t1.home_dir,
                        t2.hostname,
                        t2.ip
                 from upgrade_user t1, upgrade_machine t2
                 where t1.machine_id=t2.id and t1.id=%s
              '''
        dic = {}
        try:
            data = self.__cursorQuery(sql, [id])
            dic['user'] = data[0][0]
            dic['password'] = data[0][1]
            dic['sshport'] = data[0][2]
            dic['home_dir'] = data[0][3]
            dic['hostname'] = data[0][4]
            dic['ip'] = data[0][5]
            return dic
        except:
            return dic

    # 更新 连接 参数
    def updateConnectStatus(self, id, isconnected):
        sql = '''update upgrade_user set isconnected=%s,connect_time=%s where id=%s'''
        try:
            self.__cursorQuery(sql, [isconnected, getUnixTimestamp(), id])
            return id
        except:
            return ''



#########################################
