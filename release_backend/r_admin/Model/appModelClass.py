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


    ##  插入接口  ##
    def __cursorInsert(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
            return int(cursor.lastrowid)
        except Exception, e:
            print "Catch exception : " + str(e)
            return ''


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

    ## 添加 应用
    def addApp(self, data):
        sql = '''insert into upgrade_app(name,user,pkgname,appdir,is_valid,project_id,port,start_sequence)
                 values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        return self.__cursorInsert(sql, [data['name'], data['user'], data['pkgname'],
                                         data['appdir'], data['is_valid'], data['project_id'],
                                         data['port'], data['start_sequence']])

    ### 添加应用 机器中间表数据
    def addAppMachine(self, app_id, machine_id):
        sql = '''insert into upgrade_app_machine(app_id,machine_id) values (%s,%s)'''
        return self.__cursorInsert(sql, [app_id, machine_id])

    # 获取应用列表接口
    def getAppList(self):
        sql = '''select t1.id,
                        t1.name,
                        t1.user,
                        t1.pkgname,
                        t1.appdir,
                        t1.is_valid,
                        t2.name as pro_name,
                        t2.remark,
                        t1.port,
                        t1.start_sequence,
                        t1.project_id,
                        t4.hostname,
                        t4.ip
                 from upgrade_app t1,release_project t2,upgrade_app_machine t3,upgrade_machine t4
                 where t1.project_id = t2.id and t3.app_id = t1.id and t3.machine_id = t4.id
            '''
        return self.__cursorQuery(sql, [])

    #删除 应用 机器中间表
    def deleteAppMachine(self, app_id):
        sql = '''delete from upgrade_app_machine where app_id=%s'''
        return self.__cursorInsert(sql, [app_id])

    # 删除应用
    def deleteApp(self, id):
        sql = '''delete from upgrade_app where id=%s'''
        return self.__cursorInsert(sql, [id])


    # 检测 包名、应用名唯一
    def checkAppName(self, appname, pkgname):
        sql = '''select name from upgrade_app where pkgname=%s'''
        data = self.__cursorQuery(sql, [pkgname])
        print 'ddddddd,is:',data
        try:
            has_appname = data[0][0]
            if has_appname != appname:
                return False
            else:
                return True
        except:
            return True

    # 根据 应用id 获取应用相关信息
    def getAppInfoById(self, id):
        sql = '''select t1.id,
                        t1.name,
                        t1.user,
                        t1.pkgname,
                        t1.appdir,
                        t1.is_valid,
                        t1.project_id,
                        t1.port,
                        t1.start_sequence,
                        t3.id as machine_id
                 from upgrade_app t1, upgrade_app_machine t2, upgrade_machine t3
                 where t1.id=t2.app_id and t2.machine_id=t3.id and t1.id=%s
              '''
        try:
            return self.__cursorQuery(sql, [id])
        except:
            return ''

    # 更新 app_machine 中间表
    def updateAppMachine(self, app_id, machine_id):
        sql = '''update upgrade_app_machine set machine_id=%s where app_id=%s'''
        try:
            self.__cursorInsert(sql, [machine_id, app_id])
            return '1'
        except:
            return ''

    # 保存应用 数据接口
    def updateApp(self, data):
        # print '0000000000:data:',data
        sql = '''update upgrade_app set name=%s,user=%s,pkgname=%s,appdir=%s,project_id=%s,port=%s,start_sequence=%s
                 where id=%s
              '''
        try:
            data = self.__cursorInsert(sql, [data['name'],
                                             data['user'],
                                             data['pkgname'],
                                             data['appdir'],
                                             data['project_id'],
                                             data['port'],
                                             data['start_sequence'],
                                             data['id']])
            return '1'
        except:
            return ''















#########################################