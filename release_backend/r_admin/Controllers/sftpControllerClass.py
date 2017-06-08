#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ..Model.sftpModelClass import *


class SftpControllerClass(object):

    # 添加 sftp 信息
    def addSftp(self, request):
        data = {}
        data['item'] = request.POST.get('item')
        data['value'] = request.POST.get('value')
        data['remark'] = request.POST.get('remark')
        project_id = request.POST.get('project_id')
        env_id = request.POST.get('env_id')
        m_sftp = SftpModelClass()
        id = m_sftp.getInsertToProjectEnvId(project_id, env_id)
        if id == '': # id 没值,需要插入中间表
            project_env_id =  m_sftp.addProjectEnv(project_id, env_id) # 插入中间表
            if project_env_id != '':
                return m_sftp.addConfig(data, project_env_id) # 插入config 表
            else:
                return ''
        else: # id 有值
            rid = m_sftp.isDuplicateData(data['item'], id) # config 是否有重复的数据
            if rid != '': # 有重复数据
                return ''
            else:
                return m_sftp.addConfig(data, id) # 没有重复数据


    # sftp 列表信息
    def sftpList(self):
        m_sftp = SftpModelClass()
        return m_sftp.sftpList()

    # 删除 sftp对应信息
    def deleteSftp(self, request):
        id = request.POST.get('id')
        m_sftp = SftpModelClass()
        return m_sftp.deleteSftp(id)

























