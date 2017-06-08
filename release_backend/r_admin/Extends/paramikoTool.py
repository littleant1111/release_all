#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能：ssh连接工具
"""
import sys
import paramiko
import os
import threading
from stat import S_ISDIR
from ..lib.pub import *


class ParamikoTool(object):

    # 构造函数
    def __init__(self):
        # self.hostname = str(dict['host'])
        # self.username = str(dict['username'])
        # self.password = str(dict['password'])
        # self.remote_dir = str(dict['remote_dir'])
        # # self.local_dir = dict['local_dir']
        # self.port = int(dict['port'])

        self.returnresult=0


    # 列出远程服务器端文件
    def listRemoteFiles(self,hostname,port,username,password,remote_dir):
        ret_list = []
        try:
            t = paramiko.Transport((str(hostname), int(port)))
            t.connect(username=str(username), password=str(password))
            sftp = paramiko.SFTPClient.from_transport(t)
            files = sftp.listdir(remote_dir+'/code/')            # 这里需要注意，列出远程文件必须使用sftp，而不能用os
            for f in files:
                # sftp.get(os.path.join(remote_dir, f), os.path.join(local_dir, f))
                ret_list.append(f)
            t.close()
        except Exception, e:
            print "Error code :[568456x], Exception : [ " + str(e) + " ]"
            ret_list = []
        return ret_list

    # 列出远程服务器端文件
    def listRemoteFilesforversion(self,version_no,hostname,port,username,password,remote_dir):
        ret_list = []
        try:
            t = paramiko.Transport((str(hostname), int(port)))
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)
            # files = sftp.listdir(self.remote_dir+'/code/'+version_no+os.sep)            # 这里需要注意，列出远程文件必须使用sftp，而不能用os

            files = sftp.listdir_attr(remote_dir+'/code/'+version_no+os.sep)
            print remote_dir+'/code/'+version_no+os.sep
            for x in files:
                filename = remote_dir+'/code/'+version_no+os.sep + '/' + x.filename  # remote_dir目录中每一个文件或目录的完整路径
                if S_ISDIR(x.st_mode):  # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
                    print filename
                    for f in sftp.listdir(filename):  # 遍历远程目录
                        ret_list.append(f)
                else:
                    ret_list.append(filename)
            t.close()
        except Exception, e:
            print "Error code :[568456x], Exception : [ " + str(e) + " ]"
            ret_list = []
        return list(set(ret_list))

    def listnextdir(self,dir):
        ret_list = []
        try:
            t = paramiko.Transport((self.hostname, self.port))
            t.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            files = sftp.listdir(self.remote_dir+os.sep+dir)            # 这里需要注意，列出远程文件必须使用sftp，而不能用os
            for f in files:
                ret_list.append(f)
            t.close()
        except Exception, e:
            print "Error code :[568456x], Exception : [ " + str(e) + " ]"
            ret_list = []
        return ret_list


    # 封装在远程机器上执行命令的接口 cmdlist = [['chmod', '+x', '/home/a.sh'], ['chmod', '+x', '/home/b.sh']
    def execCommandInRemoteHost(self, ip, username, port, password, *cmdlist):
        if len(cmdlist) == 0:
            print "======  execCommandInRemoteHost parameters error  ========"
            return 'false'
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(ip), int(port), str(username), str(password))
            for i in range(len(cmdlist)):
                cmd = ''
                for j in range(len(cmdlist[i])):
                    cmd += '{0} '.format(cmdlist[i][j])
                stdin, stdout, stderr = ssh.exec_command(command=cmd)
                channel = stdout.channel
                status = channel.recv_exit_status()
                print status
                err = stderr.read()  # 标准错误输出
                try:
                    if err != '':
                        print "=========== 错误信息 1：" + str(err).decode('utf-8')
                        self.returnresult+=1
                        return 'false'
                    else:
                        stdread = stdout.read().decode('utf-8')
                        print "===== 输出信息 ：[ " + str(stdread) + " ] ======"
                except Exception, e:
                    print "=========== 错误信息 3：" + str(e)
                    self.returnresult += 1
                    return 'false'
            ssh.close()
        except Exception, e:
            print "=========== 错误信息 4：" + str(e)
            self.returnresult += 1
            return 'false'
        return 'true'

    # 判断远程目录是否存在
    def remoteHostHasDir(self, ip, username, sshport, password, dirname):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, sshport, username, password)
            command = 'cd {0}'.format(dirname)
            stdin, stdout, stderr = ssh.exec_command(command=command)
            err = stderr.read()
            ssh.close()
            try:
                if err != '':
                    print "=========== 提示信息 1：" + str(err).decode('utf-8')
                    return 'false'
                else:
                    stdread = stdout.read().decode('utf-8')
                    print "===== 输出信息 ：[ " + str(stdread) + " ] ======"
                    return 'true'
            except Exception, e:
                print "=========== 错误信息 3：" + str(e).decode('utf-8')
                return 'false'
        except Exception, e:
            print "=========== 错误信息 4：" + str(e)
            return 'false'


    # 多线程执行命令 lst = [[u'10.80.7.78', u'beehive', 10022L, u'beehive_1', [u'/auto_deploy/201701181008_1484729210/LoginSYS/script/bin/a.sh']], [u'10.80.7.79', u'beehive', 10022L, u'beehive_1', [u'/auto_deploy/201701181008_1484729210/LoginSYS/script/bin/a.sh']]]
    def runRemoteScriptProcess(self, *lst):
        threads = []
        try:
            for i in range(len(lst)):
                host, user, port, password, cmds= lst[i][0], lst[i][1], lst[i][2], lst[i][3], lst[i][4]
                threads.append(threading.Thread(target=self.execCommandInRemoteHost,
                                                    args=(host,user,port,password,cmds)))
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                if t.isAlive():
                    t.join()
            print 'result__', self.returnresult,lst
            if self.returnresult==0:
                return 'true'
            else:
                return 'false'
        except Exception, e:
            print "[ERROR] runRemoteScriptProcess Exception : [ " + str(e) + " ]"
            return 'false'


    # 下载远程目录下的文件
    def sftp_download(self, host, username, port, password, local, remote):
        if remote[-1] != '/':
            remote += '/'
        if local[-1] != '/':
            local += '/'
        sf = paramiko.Transport((str(host),int(port)))
        sf.connect(username = str(username),password = str(password))
        sftp = paramiko.SFTPClient.from_transport(sf)
        try:
            for f in sftp.listdir(remote):                              # 遍历远程目录
                print "[INFO] is downloading remote file:", os.path.join(remote+f)
                sftp.get(os.path.join(remote+f), os.path.join(local+f)) # 下载目录中文件
                print "[INFO] download successed . remote file:", os.path.join(remote + f)
        except Exception,e:
            print 'sftp_download download exception:',e
            return False
        sf.close()
        return True


    # 循环遍历 目录下所有文件#



    # 获取远端linux主机上指定目录及其子目录下的所有文件------
    def __get_all_files_in_remote_dir(self, sftp, remote_dir):
        all_files = []             # 保存所有文件的列表
        if remote_dir[-1] == '/':  # 去掉路径字符串最后的字符'/'，如果有的话
            remote_dir = remote_dir[0:-1]

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = sftp.listdir_attr(remote_dir)
        for x in files:
            filename = remote_dir + '/' + x.filename  # remote_dir目录中每一个文件或目录的完整路径
            if S_ISDIR(x.st_mode):                    # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
                all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)
        return all_files

    # 获取远程目录及目录下子目录及文件
    def sftp_get_dir(self, host, username, port, password, local_dir, remote_dir):
        t = paramiko.Transport(str(host), int(port))
        t.connect(username=str(username), password=str(password))
        sf = paramiko.SFTPClient.from_transport(t)
        if remote_dir[-1] != '/':
            remote_dir += '/'
        # 获取远端linux主机上指定目录及其子目录下的所有文件, 返回的 all_files 包含了 remote_dir
        all_files = self.__get_all_files_in_remote_dir(sf, remote_dir)
        print 'all_files is:', all_files
        try:
            for x in all_files: # 依次get每一个文件
                relative_paths = x.split(remote_dir)[1].split('/')[0:-1]
                relative_path = ''
                for each_p in relative_paths:
                    if relative_path == '':
                        relative_path = each_p
                    else:
                        relative_path = relative_path + '/' + each_p
                filename = x.split('/')[-1]
                local_file_dir = local_dir + '/' + relative_path # create local dir
                cmds = [['mkdir', '-p', local_file_dir]]
                if execShellCommand(*cmds) == False:
                    return False
                local_filename = os.path.join(local_file_dir, filename)
                # print u'Get文件%s传输中...' % filename
                print "[INFO] is downloading remote file:", x
                sf.get(x, local_filename)
                print "[INFO] download successed . download to local dir file:", os.path.join(local_file_dir, filename)
        except Exception,e:
            print 'sftp_get_dir download exception:',e
            return False
        sf.close()
        return True




