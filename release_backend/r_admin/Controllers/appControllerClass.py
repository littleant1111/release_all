#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Model.appModelClass import *
import json

class AppControllerClass(object):

    #添加应用
    def addApp(self, request):
        data = {}
        data['name'] = request.POST.get('name')
        data['user'] = request.POST.get('user')
        data['pkgname'] = request.POST.get('pkgname')
        data['appdir'] = request.POST.get('dir')
        data['is_valid'] = 1
        data['port'] = request.POST.get('port')
        data['start_sequence'] = request.POST.get('seqence')
        data['project_id'] = request.POST.get('project_id')
        data['machine_id'] = request.POST.get('machine_id')

        m_app = AppModelClass()
        app_id = m_app.addApp(data)
        if app_id !='':
            return m_app.addAppMachine(app_id, data['machine_id'])
        else:
            return ''

    # 应用列表
    def getAppList(self):
        m_app = AppModelClass()
        return m_app.getAppList()

    # 删除应用
    def deleteApp(self, request):
        id = request.POST.get('id')
        m_app = AppModelClass()
        r_id = m_app.deleteAppMachine(id)
        if r_id != '':
            return m_app.deleteApp(id)
        else:
            return ''

    # 检测 包名、应用名唯一
    def checkAppName(self, request):
        appname = request.POST.get('appname')
        pkgname = request.POST.get('pkgname')
        m_app = AppModelClass()
        return m_app.checkAppName(appname, pkgname)

    # 获取应用相关信息
    def getAppInfoById(self, request):
        id = request.GET.get('id')
        m_app = AppModelClass()
        return m_app.getAppInfoById(id)



    # 更新 应用
    def updateApp(self, request):
        data = json.loads(request.body)
        m_app = AppModelClass()
        if m_app.updateAppMachine(data['id'], data['machine_id']) == '1':
            return m_app.updateApp(data)
        else:
            return ''










