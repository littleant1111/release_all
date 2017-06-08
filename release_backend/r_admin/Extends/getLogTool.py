#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/6 13:49
# @Author  : WangZi
# @Qq      : 277215243 
# @File    : getLogTool.py
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import sys
import paramiko
import os
reload(sys)
sys.setdefaultencoding('gbk')

class GetLogTool(object):

###{'username': u'beehive', 'ip': u'10.80.7.78', 'app': u'LoginSYS', 'stepname': u'upload', 'password': u'beehive_1', 'port': 10022L}###
    def __init__(self, **dict):
        """
        初始化工具类获取必要参数
        :param port:
        :param dict:
        """
        self.ip = dict['ip']
        self.username = dict['username']
        self.password = dict['password']
        self.port = dict['port']
        self.app = dict['app']
        step_bindic = {'check':'checkapp.sh.log','backup':'backupapp.sh.log','app_stop':'stopapp.sh.log',
                       'upgrade':'updateapp.sh.log','app_start':'startapp.sh.log','rollback':'rollbackapp.sh.log'}



        self.stepname = step_bindic[dict['stepname']]
        self.taskdir = dict['taskdir']
        self.log_file = '/auto_deploy'+os.sep+self.taskdir+os.sep+self.app+os.sep+'script'+os.sep+'log'+os.sep+self.stepname
        # self.log_file = '/auto_deploy/'+


    def getlogallrow(self):
        """
        获取远端服务器日志所有内容
        :return:
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, self.port, self.username, self.password)
            command = 'tail -n 500 {0}'.format(self.log_file)
            stdin, stdout, stderr = ssh.exec_command(command=command)
            err = stderr.read()
            ssh.close()
            try:
                if err != '':
                    return str(err).decode('utf-8')
                else:
                    if self.ip=='10.25.1.40' or self.ip=='10.25.1.35':
                        stdread = stdout.read().decode('gbk')
                    else:
                        stdread = stdout.read().decode('utf-8')
                    return stdread
            except Exception, e:
                print e
                if err != '':
                    return str(err)
                else:
                    stdread = stdout.read()
                    print stdread

                    return stdread
        except Exception, e:
            return str(e)

