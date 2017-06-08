#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import connection

class FtpModelClass(object):

    ##  查询接口  ##
    def __cursorQuery(self, sql, parlist):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, parlist)
        except Exception,e:
            print "Catch exception : " + str(e)
        return cursor.fetchall()

    ## 根据 配置项名称、项目编码/名称、环境名称 获取对应的配置项值  ###
    def getvalue(self, itemname, project_no, env_name):

        sql = """select value
                    from release_config t1, release_project t2, release_env_child t3,release_project_env_child t4
                    where item=%s and t4.project_id=t2.id and t2.name=%s and t4.env_child_id=t3.id and t3.envchild_name=%s
                     and t4.id=t1.project_env_id"""
        rows = self.__cursorQuery(sql,[itemname, project_no, env_name])
        if len(rows)!=0:
            value = rows[0][0]
            return value
        else:
            return ''


    #### 获取 蜂巢 sit sftp 连接配置信息  #####
    def getFcSitFtpConifgToDic(self):
        dic = {}
        dic['host'] = self.getvalue('sftp_host', 'HCS', 'sit')
        dic['username'] = self.getvalue('sftp_user', 'HCS', 'sit')
        dic['port'] = self.getvalue('sftp_port', 'HCS', 'sit')
        dic['password'] = self.getvalue('sftp_pass', 'HCS', 'sit')
        dic['remote_dir'] = self.getvalue('sftp_basedir', 'HCS', 'sit')
        # print "config dic : ", dic
        return dic

    ## 根据 项目编码、 环境类型 获取 sftp 连接配置信息 ,参数如： HCS  sit
    def getProjectEnvConnectsInfo(self,  env_name,project_no):
        dic = {}
        dic['host'] = self.getvalue('sftp_host', str(project_no), str(env_name))
        dic['username'] = self.getvalue('sftp_user', str(project_no), str(env_name))
        dic['port'] = self.getvalue('sftp_port', str(project_no), str(env_name))
        dic['password'] = self.getvalue('sftp_pass', str(project_no), str(env_name))
        dic['remote_dir'] = self.getvalue('sftp_basedir', str(project_no), str(env_name))
        return dic

        ## 根据 项目编码、 环境类型 获取 sftp 连接配置信息 ,参数如： HCS  sit
        def getProjectPkgInfo(self, env_name, project_no):
            dic = {}
            dic['host'] = self.getvalue('sftp_host', str(project_no), str(env_name))
            dic['username'] = self.getvalue('sftp_user', str(project_no), str(env_name))
            dic['port'] = self.getvalue('sftp_port', str(project_no), str(env_name))
            dic['password'] = self.getvalue('sftp_pass', str(project_no), str(env_name))
            dic['remote_dir'] = self.getvalue('sftp_basedir', str(project_no), str(env_name))
            return dic

#########################################