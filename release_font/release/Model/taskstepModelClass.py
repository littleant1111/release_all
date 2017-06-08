#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import connection
from ..lib.pub import *
import time

class TaskstepModelClass(object):

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
        # return cursor.fetchall()


    def __cursorUpdate(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
            return int(cursor.lastrowid)
        except Exception,e:
            print "Catch exception : " + str(e)
            return ''
        # return cursor.fetchall()


    def updateisstop(self,status,id):
        sql="""update task_step set is_stoped=%s where id=%s"""
        id=self.__cursorUpdate(sql,[status,id])
        return id


    def updatestep(self,taskid,stepid,status):
        if status==2:
            sql="""update task_step set status=%s,end_time=%s where task_id=%s and step_id=%s"""
            id=self.__cursorUpdate(sql,[status,int(time.time()),taskid,stepid])
        if status==1:
            sql="""update task_step set status=%s,start_time=%s where task_id=%s and step_id=%s"""
            id=self.__cursorUpdate(sql,[status,int(time.time()),taskid,stepid])
        else:
            sql="""update task_step set status=%s where task_id=%s and step_id=%s"""
            id=self.__cursorUpdate(sql,[status,taskid,stepid])
        return id

    def getnextstopstatus(self,taskid,stepid):
        sql1="""select id from task_step where task_id=%s and step_id=%s"""
        iddata=self.__cursorQuery(sql1,[taskid,stepid])
        nextid=int(iddata[0][0])+1
        sql2="""select is_stoped,step_id from task_step where id=%s"""
        data=self.__cursorQuery(sql2,[nextid])
        return data[0]





    # 根据 app / app_db / db 获取到 改执行的步骤
    def getStepsByAppDbStr(self, ab_str):
        ret_list = []
        sql1 = 'select id \
                from upgrade_step \
                where is_valid=1 and app_db_str=%s or app_db_str=%s \
                order by sort asc'
        sql2 = 'select id \
                from upgrade_step \
                where is_valid=1 and app_db_str=%s \
                order by sort asc'
        if ab_str == 'app' or ab_str == 'db':
            ids = self.__cursorQuery(sql1, [ab_str, 'app_db'])
        elif ab_str == 'app_db':
            ids = self.__cursorQuery(sql2, [ab_str])
        else:
            ids = ''
            print "Can not get step .."
            return ''
        if len(ids) != 0:
            for i in range(len(ids)):
                ret_list.append(ids[i][0])
        return ret_list


    # 根据 app_db app db 来插入到任务步骤表数据
    def addDataToTaskStepByStr(self, task_id, ab_str):
        ret_list = self.getStepsByAppDbStr(ab_str)
        start_time = getUnixTimestamp()
        if len(ret_list) > 0 :
            for i in range(len(ret_list)):
                step_id = ret_list[i]
                lastid = self.insertIntoTaskStep(task_id, step_id, start_time, end_time=0, is_stoped=0)
                if lastid == '':
                    print "Insert data failed , data = [ " + str(task_id) + str(step_id) + str(start_time) + " to table : task_step failed ."
                    return 'false'
            return 'true'
        else:
            return 'false'

    # 插入到task_step 数据
    def insertIntoTaskStep(self, task_id, step_id, start_time, end_time, is_stoped):
        if int(step_id)==7:
            sql = 'insert into task_step (task_id,step_id,start_time,end_time,is_stoped) values (%s,%s,%s,%s,%s)'
            id = self.__cursorInsert(sql, [task_id, step_id, start_time, end_time, '1'])
        else:
            sql = 'insert into task_step (task_id,step_id,start_time,end_time,is_stoped) values (%s,%s,%s,%s,%s)'
            id = self.__cursorInsert(sql, [task_id, step_id, start_time, end_time, is_stoped])


        return id

    # 更步骤表 is_stoped 状态
    def changeIsStopedValue(self, taskid, stepname):
        return True


    # 获取 对应步骤 的 is_stoped 状态
    def getIsStopedStatus(self, taskid, stepid):
        sql = '''select is_stoped from task_step where task_id=%s and step_id=%s'''
        data = self.__cursorQuery(sql, [taskid, stepid])
        if len(data) == 0:
            return ''
        return data[0][0]

    # 根据 taskid 和 步骤名称 获取 对应的 is_stoped 状态
    def getIsStopedStatus2(self, taskid, stepname):
        sql = '''select t1.is_stoped
                    from task_step t1, upgrade_step t2
                    where t1.task_id=%s and t2.id=t1.step_id and t2.name=%s'''
        data = self.__cursorQuery(sql, [taskid, stepname])
        if len(data) == 0:
            return ''
        return str(data[0][0]).strip()

    # 获取当前任务步骤的执行顺序, 返回列表 [[taskid, stepid, 步骤名称], [taskid, stepid, 'check'], ...]
    def getTaskStepSequence(self, taskid):
        sql = '''select t1.task_id, t1.step_id, t2.name
                    from task_step t1, upgrade_step t2
                    where t1.task_id=%s and t1.step_id=t2.id
                    order by t1.id asc'''
        data = self.__cursorQuery(sql, [taskid])
        if len(data) == 0:
            print "[ERROR] Data is null. "
            return ''
        return list(data)

    #通过taskid获取详情页###
    def getdetailbytaskid(self,taskid):
        sql = """select t1.id,t2.name,t2.remark,t2.comments,t1.status,t1.is_stoped from
              task_step t1,upgrade_step t2 where t1.task_id=%s and t1.step_id=t2.id"""
        data = self.__cursorQuery(sql, [taskid])
        ret_list=[]
        for i in range(len(data)):
            dic={}
            dic['id'] = str(data[i][0])
            dic['name'] = data[i][1]
            dic['remark'] = data[i][2]
            dic['comments'] = data[i][3]
            dic['status'] = data[i][4]
            dic['is_stoped'] = str(data[i][5])
            ret_list.append(dic)
        if len(data) == 0:
            print "[ERROR] Data is null. "
            return ''
        return ret_list

    ##根据step id 得到 上一步statu，和本步is_stoped状态##
    def getstatuisstopbyid(self,id):

        ret_dic = {}
        sql = """select step_id from task_step where id=%s"""
        data = self.__cursorQuery(sql, [id])
        if int(data[0][0]) != 8:
            sql="""select status from task_step where id=%s"""
            data = self.__cursorQuery(sql, [str(int(id)-1)])
            if int(data[0][0])!=2:
                ret_dic['result'] = 'false'
                ret_dic['msg'] = '上一步未完成，请检查！'
                return ret_dic
        sql = """select is_stoped from task_step where id=%s"""
        data = self.__cursorQuery(sql, [id])
        if int(data[0][0])==1:
            ret_dic['result'] = 'false'
            ret_dic['msg'] = '本步骤禁止执行，请检查!'
            return ret_dic
        ret_dic['result'] = 'true'
        ret_dic['msg'] = ''
        return ret_dic


    ## 根据 taskid查询 id和status ##

    def getidstatusbytaskid(self,taskid):
        sql="""select status,id from task_step where task_id=%s"""
        data = self.__cursorQuery(sql, [taskid])
        if len(data) == 0:
            print "[ERROR] Data is null. "
            return ''
        ret_list=[]
        for da in data:
            dic={}
            dic['status'] = str(da[0])
            dic['id'] = str(da[1])
            ret_list.append(dic)
        return ret_list

    ## 根据task_stepid 获取 对应步骤名
    def getnamebytaskid(self, taskid):
        sql = """select t2.`name` from task_step t1, upgrade_step t2 where t1.id=%s and t1.step_id=t2.id"""
        data = self.__cursorQuery(sql, [taskid])
        if len(data) != 0:
            return data[0][0]
        else:
            return ''

    def getmintimebyid(self, taskid):
        sql = """select min(start_time) from task_step t1 where t1.task_id=%s"""
        data = self.__cursorQuery(sql, [taskid])
        if len(data) != 0:
            return data[0][0]
        else:
            return ''

    def getmaxtimebyid(self, taskid):
        sql = """select max(end_time) from task_step t1 where t1.task_id=%s"""
        data = self.__cursorQuery(sql, [taskid])
        if len(data) != 0:
            return data[0][0]
        else:
            return ''

    def getstatus(self, taskid):
        sql = """select status from task_step t1 where t1.task_id=%s and t1.step_id=6"""
        data = self.__cursorQuery(sql, [taskid])
        if len(data) != 0:
            return data[0][0]
        else:
            return ''
            #########################################