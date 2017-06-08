#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    从ftp 上获取到对应相关信息
'''

from ..Model.ftpModelClass import *
from ..Model.taskModelClass import *
from ..Extends.paramikoTool import *
from ..lib.pub import *


class FtpControllerClass(object):

    # 获取FTP 配置信息
    def getFtpConfig(self,env_name,project_no):
        m_ftp = FtpModelClass()
        data = m_ftp.getProjectEnvConnectsInfo(env_name,project_no)
        # print "dataconfig is :xx", data
        return data

    # 根据 选择的项目 从Ftp上获取应用包名 列表返回
    def getAppPkgNameByProjectName(self,env_name,project_no,version_no):
        dic = self.getFtpConfig( env_name,project_no)
        t_paramiko = ParamikoTool()
        data = t_paramiko.listRemoteFilesforversion(version_no,dic['host'],dic['port'] ,dic['username'], dic['password'],dic['remote_dir'])
        # print "datais ,,,", data
        return data

    def getVersionByProjectName(self,env_name,project_no):
        dic = self.getFtpConfig(env_name,project_no)
        t_paramiko = ParamikoTool()
        data = t_paramiko.listRemoteFiles( dic['host'],dic['port'] ,dic['username'], dic['password'],dic['remote_dir'])
        # print "datais ,,,", data
        return data
    # 从 sftp/ftp 上下载包到指定目录,并且将配置文件和代码合并成一个包后移动到指定目录
    def downLoadPkgs(self, project_no, version, appname, taskid, **dic): # 参数为 项目编码、项目版本号、应用名称、任务ID、 sftp连接配置字典信息
        m_task = TaskModelClass()
        dir_name = m_task.getTaskDirNameById(taskid)
        target_pkgdir = os.path.dirname(os.path.abspath(__file__)) + '/../../tasks/' + dir_name + '/pkg'
        base_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../tasks/' + dir_name + '/downloads/' + str(project_no)
        download_pkg_dir = base_dir + '/code/' + str(version) + '/' + appname
        download_cfg_dir = base_dir + '/config/' + str(version) + '/' + appname
        # print "target_pkgdir1111111111 :", target_pkgdir
        cmds = [['mkdir', '-p', target_pkgdir], ['mkdir', '-p', download_pkg_dir], ['mkdir', '-p', download_cfg_dir]]
        if execShellCommand(*cmds) != True:
            return False
        pt = ParamikoTool()
        pkg_remote_dir = str(dic['remote_dir']) + '/code/' + str(version) + '/' + str(appname)
        cfg_remote_dir = str(dic['remote_dir']) + '/config/' + str(version) + '/' + str(appname)
        # return pt.sftp_download(dic['host'], dic['username'], dic['port'], dic['password'], target_pkgdir, pkg_remote_dir)
        if pt.sftp_get_dir(dic['host'], dic['username'], dic['port'], dic['password'], download_pkg_dir, pkg_remote_dir) == False:
            return False
        if pt.sftp_get_dir(dic['host'], dic['username'], dic['port'], dic['password'], download_cfg_dir, cfg_remote_dir) == False:
            return False

        # 合并配置文件和包
        combine_script = os.path.dirname(os.path.abspath(__file__)) + '/../../tasks/server/bin/combinePkgCfg.sh'
        cmds = [['chmod', '+x', combine_script], [combine_script, dir_name, download_pkg_dir, download_cfg_dir, target_pkgdir]]
        return execShellCommand(*cmds)








