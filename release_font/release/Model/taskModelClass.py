#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    任务模型获取 任务相关信息返回
'''
from ..lib.pub import *

from django.db import connection

class TaskModelClass(object):


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

    #### 得到当前任务唯一的目录名称 #
    def getTaskDirNameById(self, taskid):
        sql = 'select dir_name from task_task where id=%s limit 1'
        data = self.__cursorQuery(sql, [taskid])
        if len(data) != 0:
            name = data[0][0]
            return name
        else:
            return ''

    def updatetaskstart(self, param):
        sql = """update task_task set  env=%s, project_code=%s, version=%s, apps=%s where id=%s"""
        id = self.__cursorUpdate(sql,param)
        return id

    def updatetaskend(self, param):
        sql = """update task_task set  create_time=%s, end_time=%s, state=%s where id=%s"""
        id = self.__cursorUpdate(sql, param)
        return id


    # 任务创建完成后，生产 task_task 表数据
    def createTaskTaskData(self):
        sql = 'insert into task_task(dir_name,create_time) values(%s,%s);'
        lastid = self.__cursorInsert(sql, [onlyDirName(), getUnixTimestamp()])
        return lastid


    # 根据应用名 获取 对应的用户 和 ip ，返回 应用名、user、ip
    def getdata1(self, app_name,env_name):
        sql = """select t1.name, t1.user, t3.ip
                    from upgrade_app t1, upgrade_app_machine t2, upgrade_machine t3,upgrade_env_machine t4,release_env_child t5
                    where t1.id=t2.app_id and t2.machine_id=t3.id and t1.name=%s and t3.id=t4.machine_id  and
                     t5.id=t4.env_id and t5.envchild_name=%s"""
        paralist = self.__cursorQuery(sql, (app_name,env_name))
        return paralist

    # 根据应用的 id 获取 应用名、user、ip
    def getAppInfo1(self, appid):
        sql = """select t1.name, t1.user, t3.ip
                    from upgrade_app t1, upgrade_app_machine t2, upgrade_machine t3
                    where t1.id=t2.app_id and t2.machine_id=t3.id and t1.id=%s"""
        paralist = self.__cursorQuery(sql, (appid,))
        return paralist

    # 根据 包名 获取 应用名, 如果为空，则返回空
    def getAppNameByWarName(self, war_name):
        sql = """select t1.name
                    from upgrade_app t1
                    where t1.pkgname=%s limit 1"""
        data = self.__cursorQuery(sql, (war_name,))
        if len(data) != 0:
            return data[0][0]
        else:
            return ''

    # 根据 ip app_name 获取配置信息 ，返回到字典
    def getconfdata(self, ip, app_name):
        sql="""select t3.name, t3.sshport, t3.password, t3.home_dir, t1.appdir, t1.pkgname,t1.start_sequence
                from upgrade_user t3, upgrade_app t1, upgrade_app_machine t2, upgrade_machine t4
                where t1.id = t2.app_id and t2.machine_id = t4.id and t1.user = t3.name and t3.machine_id = t4.id and t1.name=%s and t4.ip=%s"""
        dic = {}
        ret_query=self.__cursorQuery(sql,(app_name,ip))
        print ret_query
        if len(ret_query) != 0:
            dic['name'], dic['sshport'], dic['password'], dic['homedir'], dic['appdir'], dic['pkgname'],dic['startsequence']=\
                ret_query[0][0], ret_query[0][1], ret_query[0][2], ret_query[0][3], ret_query[0][4], ret_query[0][5],ret_query[0][6]
        return dic


    def gethistoryall(self):
        sql = """select id,env,project_code,version,apps,create_time,end_time,state from task_task where state<>'0'"""
        data = self.__cursorQuery(sql, [])
        if len(data) != 0:
            return data
        else:
            return ''

    def getbsdetail(self,envchild_name):
        if envchild_name==None:
            sql = """select t1.envchild_name,t2.name,t3.name,t4.ip,t3.`user`,t3.appdir from release_env_child t1,release_project t2,upgrade_app t3,upgrade_machine t4 ,
            release_project_env_child t5,upgrade_app_machine t6,upgrade_env_machine t7
            where t1.id=t5.env_child_id and t2.id=t5.project_id
            and t2.id=t3.project_id and t3.id=t6.app_id and t4.id=t6.machine_id
            and t1.id=t7.env_id and t4.id=t7.machine_id"""
            data = self.__cursorQuery(sql, [])
        else:
            sql = """select t1.envchild_name,t2.name,t3.name,t4.ip,t3.`user`,t3.appdir from release_env_child t1,release_project t2,upgrade_app t3,upgrade_machine t4 ,
    release_project_env_child t5,upgrade_app_machine t6,upgrade_env_machine t7
    where t1.id=t5.env_child_id and t2.id=t5.project_id and t1.envchild_name=%s
    and t2.id=t3.project_id and t3.id=t6.app_id and t4.id=t6.machine_id
    and t1.id=t7.env_id and t4.id=t7.machine_id"""
            data = self.__cursorQuery(sql, [envchild_name])
        if len(data) != 0:
            return data
        else:
            return ''


#########################################
# if __name__=='__main__':
#     tscl=TaskModelClass()
#     tscl.getAppNameByWarName('beehive.war')
