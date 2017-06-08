#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ..Model.envModelClass import *
import json

class EnvControllerClass(object):

    # 获取环境信息
    def getEnvInfo(self):
        m_env = EnvModelClass()
        return m_env.getEnvInfo()

    # 获取所有环境信息
    def getEnvInfo2(self):
        m_env = EnvModelClass()
        return m_env.getEnvInfo2()

    # 添加环境
    def addEnv(self, request):
        name = request.POST.get('name')
        env = request.POST.get('env')
        m_env = EnvModelClass()
        return m_env.addEnv(name, env)

    # 删除 环境信息
    def deleteEnv(self,request):
        id = request.POST.get('id')
        m_env = EnvModelClass()
        return m_env.deleteEnv(id)

    # 编辑 环境
    def edit_env(self, request):
        id = request.GET.get('id')
        m_env = EnvModelClass()
        return m_env.getEnvInfoById(id)

    # 更新 环境
    def updateEnv(self, request):
        data = json.loads(request.body)
        m_env = EnvModelClass()
        return m_env.updateEnv(data)



















