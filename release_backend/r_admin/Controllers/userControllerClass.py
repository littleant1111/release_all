#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Model.userModelClass import *
import json
from ..Extends.paramikoTool import *

class UserControllerClass(object):

    # 获取环境信息
    def addUser(self, request):
        data = {}
        data['name'] = request.POST.get('user')
        data['password'] = request.POST.get('password')
        data['home_dir'] = request.POST.get('homedir')
        data['sshport'] = request.POST.get('sshport')
        data['machine_id'] = request.POST.get('machine_id')
        m_user = UserModelClass()
        return m_user.addUser(data)


    # 获取用户列表数据
    def getUserList(self):
        m_user = UserModelClass()
        return m_user.getUserList()


    # 检测用户在主机上是否已经存在
    def checkUserMachineExists(self, request):
        user = request.POST.get('user')
        machine_id = request.POST.get('machine_id')
        m_user = UserModelClass()
        isExists = m_user.checkUserMachineExists(user, machine_id)
        if isExists == True:
            return False
        else:
            return True


    # 删除用户
    def deleteUser(self, request):
        id = request.POST.get('id')
        m_user = UserModelClass()
        return m_user.deleteUser(id)


    # 根据 user id 获取用户信息
    def getUserInfoById(self, request):
        id = request.GET.get('id')
        m_user = UserModelClass()
        return m_user.getUserInfoById(id)


    # 保存用户
    def updateUser(self, request):
        data = json.loads(request.body)
        m_user = UserModelClass()
        return m_user.updateUser(data)


    # 检测用户连接性
    def testConnect(self, request):
        id = request.POST.get('id')
        m_user = UserModelClass()
        connectInfo = m_user.getConnectInfo(id)
        paramiko = ParamikoTool()
        isconnect = paramiko.remoteHostHasDir(connectInfo['ip'], connectInfo['user'], connectInfo['sshport'],connectInfo['password'],connectInfo['home_dir'])
        if isconnect == 'true':
            isconnected = 1
        else:
            isconnected = 0
        m_user.updateConnectStatus(id, isconnected)
        return isconnect










