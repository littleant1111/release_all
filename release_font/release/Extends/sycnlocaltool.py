#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
from ..Model.taskModelClass import *
import paramikoTool
from ..lib.pub import *

class sycnlocaltool(object):

    @staticmethod
    def syncloacl(retlist, dir_name):
        # print 'retlist is :',retlist
        REMOTE_BASE_DIR = '/auto_deploy/'
        if REMOTE_BASE_DIR[-1] != '/':
            REMOTE_BASE_DIR += '/'
        task_path = os.path.dirname(os.path.abspath(__file__)) + '/../../tasks'
        # print "yyyyyyyyyy:", task_path
        timedir = task_path + '/{0}'.format(dir_name)
        taskmdcl = TaskModelClass()
        for data in retlist: # [[(u'LoginSYS', u'beehive', u'10.80.7.78'), 'project1','v001001'], ...]
            appname = data[0][0]
            ip = data[0][2]
            dic = taskmdcl.getconfdata(ip, appname)  # 获取配置信息
            pt=paramikoTool.ParamikoTool()
            pkg_file = timedir + '/pkg/' + dic['pkgname']
            local_appname_dir = timedir + '/' + ip + '/' + appname
            local_app_pkg_dir = timedir + '/' + ip + '/' + appname + '/pkg'
            scriptdir = timedir + '/' + ip + '/' + appname + '/script'

            cmds = [['mkdir', '-p', scriptdir],                                    # 创建脚本目录
                    ['mkdir', '-p', local_app_pkg_dir],                            # 创建本地存包目录
                    ['cp', '-f', pkg_file, local_app_pkg_dir],                     # 拷贝发布的包到指定目录
                    ['cp', '-rf', task_path + '/client/*', scriptdir + '/'],       # 拷贝文件
                    ['chmod', '+x', task_path + '/server/bin/execRsync.exp']]      # 同步脚本加权限
            if execShellCommand(*cmds) != True: # 本地运行命令
                print 'local command'
                return 'false'

            test_remote_dir = REMOTE_BASE_DIR  + dir_name
            if pt.remoteHostHasDir(ip, dic['name'], dic['sshport'], dic['password'], test_remote_dir) == 'false':
                cmd_lst = [
                    ['mkdir', '-p', REMOTE_BASE_DIR  + dir_name],
                    ['chmod', '777', REMOTE_BASE_DIR + dir_name],
                    ['mkdir', '-p', REMOTE_BASE_DIR  + dir_name + '/' + appname + '/script']]
            else:
                cmd_lst = [['mkdir', '-p', REMOTE_BASE_DIR + dir_name + '/' + appname + '/script']]
            ret = pt.execCommandInRemoteHost(ip, dic['name'], dic['sshport'], dic['password'], *cmd_lst) #远程执行
            if ret != 'true':
                print 'ret'
                return ret

            # 写入配置文件
            f = open(scriptdir + '/conf/app_config.conf', 'w') # 开始写入配置文件
            f.write('pkgfile={0}'.format(REMOTE_BASE_DIR + dir_name + '/'  + appname + '/pkg/' + dic['pkgname']) + '\n')
            f.write('version={0}'.format(data[2]) + '\n')
            f.write('appnumber={0}'.format('1') + '\n')
            f.write('projectname={0}'.format(data[1]) + '\n')
            f.write('ip={0}'.format(ip) + '\n')
            f.write('user[1]={0}'.format(dic['name']) + '\n')
            f.write('upgradetype[1]=full' + '\n')
            f.write('apptype[1]=tomcat' + '\n')
            f.write('backupdir[1]={0}'.format(REMOTE_BASE_DIR + dir_name + '/' + appname + '/backup') + '\n')
            f.write('appdir[1]={0}'.format(dic['appdir']) + '\n')
            f.write('appwarname[1]={0}'.format(dic['pkgname']) + '\n')
            f.write('startuptime[1]=1000' + '\n')
            f.write('port[1]=8080' + '\n')
            f.close() # 写入配置文件完成

            # connect_lst = [ip, dic['name'], dic['sshport'], dic['password'], scriptdir, REMOTE_BASE_DIR + dir_name + '/' + appname + '/']
            connect_lst = [ip, dic['name'], dic['sshport'], dic['password'], local_appname_dir, REMOTE_BASE_DIR + dir_name + '/']
            if rsyncServerToClients(task_path + '/server/bin/execRsync.exp', *connect_lst) != True:
                print 'rsyncServerToClients'
                return 'false'

            cmds = [['chmod', '+x', REMOTE_BASE_DIR + dir_name + '/' + appname + '/script/bin/*.sh']] # *.sh 加执行权限
            ret = pt.execCommandInRemoteHost(ip, dic['name'], dic['sshport'], dic['password'], *cmds)
            if ret != 'true':
                print 'execCommandInRemoteHost'
                return ret
        return 'true'

    @staticmethod
    def runStep(retlist, dir_name, stepname):
        if stepname not in ['check', 'backup', 'app_stop', 'exec_sql', 'upgrade', 'app_start', 'rollback']:
            print '[ERROR] runStep paramters error .'
            return 'false'
        REMOTE_BASE_DIR = '/auto_deploy/'
        if REMOTE_BASE_DIR[-1] != '/':
            REMOTE_BASE_DIR += '/'
        taskmdcl = TaskModelClass()
        conncets_list = []
        for data in retlist:
            appname, ip = data[0][0], data[0][2] # 应用名、ip
            if stepname == 'check':
                remote_script = 'checkapp.sh'
            elif stepname == 'backup':
                remote_script = 'backupapp.sh'
            elif stepname == 'app_stop':
                remote_script = 'stopapp.sh'
            elif stepname == 'upgrade':
                remote_script = 'updateapp.sh'
            elif stepname == 'app_start':
                remote_script = 'startapp.sh'
            elif stepname == 'rollback':
                remote_script = 'rollbackapp.sh'
            else:
                print "=======  not konw this step.  ========"
                return 'false'
            # remote_script = 'a.sh'                   # 测试代码
            dic = taskmdcl.getconfdata(ip, appname)  # 获取配置信息
            conncets = [ip, dic['name'], dic['sshport'], dic['password'],
                    [REMOTE_BASE_DIR + dir_name + '/' + appname + '/script/bin/'+ remote_script],dic['startsequence'],appname]
            conncets_list.append(conncets)

        print "conncets_list 999999999999:", conncets_list
        pt = paramikoTool.ParamikoTool()


        if stepname == 'app_start':
            tuplelist = []
            for conncet in conncets_list:
                tuplelist.append(conncet[5])
            if len(list(set(tuplelist))) == 1:
                print 'all_run...',conncets_list
                return pt.runRemoteScriptProcess(*conncets_list)
            newlst = []  # 新列表
            numdct = {}  # 带下标数字字典
            seqlst = []  # 序号列表
            for i in range(len(conncets_list)):
                # for j in range(len(orglst[i])):
                if not numdct.has_key(i):
                    numdct[i] = {}
                    numdct[i] = conncets_list[i][5]
            print 'numlist', numdct

            # dic = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
            seqdct = sorted(numdct.items(), key=lambda d: d[1], reverse=False)
            print seqdct

            for j in range(len(seqdct)):
                seqlst.append(seqdct[j][0])
            print 'seqlst', seqlst

            for i in range(len(seqlst)):
                newlst.append(conncets_list[seqlst[i]])
            print 'newlst', newlst
            print '-----------------------------------------------'
            # print 'len_newlst', len(newlst)

            all_seq_lst = []  # 存放最后的list
            i = 0  # 初始化
            while (i < len(newlst)):  # 循环i直到到列表最后
                print 'loop', i
                tmp_lst = []
                tmp_lst.append(newlst[i])
                for j in range(i + 1, len(newlst)):  # 从i+1个开始循环
                    # if newlst[i][5] == newlst[j][5] and newlst[i][6] == newlst[j][6]:  # 当前数值与下一个相等，并且应用相同
                    if newlst[i][5] == newlst[j][5]:  # 当前数值与下一个相等，并且应用相同

                        tmp_lst.append(newlst[j])
                        i += 1
                        continue
                all_seq_lst.append(tmp_lst)
                i += 1
            print 'all_seq_lst', all_seq_lst
            result='false'
            count=0
            for seqlist in all_seq_lst:
                count=count+1
                print 'seq....',seqlist,len(seqlist),'seq=',count

                if len(seqlist)==1:
                    print 'one........',seqlist
                    if 'true'== pt.execCommandInRemoteHost(seqlist[0][0], seqlist[0][1], seqlist[0][2], seqlist[0][3], seqlist[0][4]):
                        result='true'
                        continue
                    else:
                        result='false'
                        break
                else:
                    print 'process.......',seqlist
                    if 'true' == pt.runRemoteScriptProcess(*seqlist):
                        result='true'
                        continue
                    else:
                        result = 'false'
                        break
            return result
        return pt.runRemoteScriptProcess(*conncets_list)
