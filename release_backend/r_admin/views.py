#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
# reload(sys)
# sys.setdefaultencoding('utf8')
# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from Controllers.loginControllerClass import *
from Controllers.projectControllerClass import *
from Controllers.machineControllerClass import *
from Controllers.envControllerClass import *
from Controllers.appControllerClass import *
from Controllers.userControllerClass import *
from Controllers.sftpControllerClass import *
from django.core import serializers


# 登录
def login(request):
    c_login = LoginControllerClass(request)
    return c_login.login()
# 退出
def logout(request):
    c_login = LoginControllerClass(request)
    return c_login.logout()
# 密码更改
def password_change(request):
    c_login = LoginControllerClass(request)
    return c_login.password_change()
# 密码更改完成
def password_change_done(request):
    return render(request, 'password_change_done.html')
# 首页
def index(request):
    c_login = LoginControllerClass(request)
    return c_login.index()

# test
def test(request):
    return JsonResponse('abc', safe=False)

# 获取 环境id,环境名称 返回 [(环境id,环境名称),('1','sit1'),('5','UAT-B')]
def getEnvInfo(request):
    c_machine = MachineControllerClass()
    data = c_machine.getEnvInfo()
    # print 'data0000:', data
    return JsonResponse(data, safe=False)

# 添加机器接口
def addMachine(request):
    c_machine = MachineControllerClass()
    id = c_machine.addMachineInfo(request)
    return JsonResponse(id, safe=False)

# 编辑机器接口
def editMachine(request):
    c_machine = MachineControllerClass()
    rdata = c_machine.updateMachine(request)
    # print 'idis ........:', rdata
    return JsonResponse(rdata, safe=False)

# 添加项目接口
def addProject(request):
    c_project = ProjectControllerClass()
    id = c_project.addProject(request)
    return JsonResponse(id, safe=False)

# 添加项目接口
def add_project(request):
    data = {}
    c_env = EnvControllerClass()
    data['env'] = c_env.getEnvInfo2()
    return render(request, 'add_project.html', {'data':data})

# 编辑项目
def edit_project(request):
    id = request.GET.get('id')
    data = {}
    c_project = ProjectControllerClass()
    data['project'] = c_project.getProjectEnvInfoById(id)
    c_env = EnvControllerClass()
    data['env'] = c_env.getEnvInfo2()
    print '999999999999', data
    return render(request, 'edit_project.html', {'data': data})

# 编辑项目
def editProject(request):
    c_project = ProjectControllerClass()
    id = c_project.updateProject(request)
    return JsonResponse(id, safe=False)

# 获取项目列表 接口
def getProjectList(request):
    c_project = ProjectControllerClass()
    data = c_project.getProjectInfo2()
    return JsonResponse(data, safe=False)


# 项目列表
def project_list(request):
    data = {}
    c_project = ProjectControllerClass()
    data['project'] = c_project.getProjectInfo2()
    # c_env = EnvControllerClass()
    # data['env'] = c_env.getEnvInfo2()
    return render(request, 'project_list.html', {'data':data})

# 删除项目 接口
def deleteProject(request):
    c_project = ProjectControllerClass()
    id = c_project.deleteProject(request)
    return JsonResponse(id, safe=False)

# 删除机器 接口
def deleteMachine(request):
    c_machine = MachineControllerClass()
    id = c_machine.deleteMachine(request)
    return JsonResponse(id, safe=False)

# 添加环境
def addEnv(request):
    # import time
    # time.sleep(2)
    c_env = EnvControllerClass()
    id = c_env.addEnv(request)
    return JsonResponse(id, safe=False)

# 环境列表
def env_list(request):
    c_env = EnvControllerClass()
    data = c_env.getEnvInfo2()
    return render(request, 'env_list.html', {'data': data})

# 删除 环境
def deleteEnv(request):
    c_env = EnvControllerClass()
    id = c_env.deleteEnv(request)
    return JsonResponse(id, safe=False)

# 添加应用
def add_app(request):
    data = {}
    c_project = ProjectControllerClass()
    data['project'] = c_project.getProjectInfo2()
    c_machine = MachineControllerClass()
    data['machine'] = c_machine.getMachineSimpleListInfo()
    return render(request, 'add_app.html', {'data':data})

# 添加应用 接口
def addApp(request):
    c_app = AppControllerClass()
    id = c_app.addApp(request)
    return JsonResponse(id, safe=False)

# 应用列表
def app_list(request):
    c_app = AppControllerClass()
    data = c_app.getAppList()
    return render(request, 'app_list.html', {'data': data})

# 删除应用
def deleteApp(request):
    c_app = AppControllerClass()
    id = c_app.deleteApp(request)
    return JsonResponse(id, safe=False)

# 编辑 应用
def edit_app(request):
    data = {}
    c_app = AppControllerClass()
    c_project = ProjectControllerClass()
    data['project'] = c_project.getProjectInfo2()
    c_machine = MachineControllerClass()
    data['machine'] = c_machine.getMachineSimpleListInfo()
    data['data'] = c_app.getAppInfoById(request)
    return render(request, 'edit_app.html', {'data': data})

# 编辑应用 接口
def editApp(request):
    c_app = AppControllerClass()
    id = c_app.updateApp(request)
    return JsonResponse(id, safe=False)

# 添加用户接口
def addUser(request):
    c_user = UserControllerClass()
    id = c_user.addUser(request)
    print id,request.body
    return JsonResponse(id, safe=False)

# 添加 sftp 配置
def add_sftp(request):
    data = {}
    c_project = ProjectControllerClass()
    data['project'] = c_project.getProjectInfo2()
    c_env = EnvControllerClass()
    data['env'] = c_env.getEnvInfo2()
    return render(request, 'add_sftp.html', {'data': data})

#  添加 sftp 接口
def addSftp(request):
    c_sftp = SftpControllerClass()
    id = c_sftp.addSftp(request)
    return JsonResponse(id, safe=False)

# sftp 配置列表
def sftp_list(request):
    c_sftp = SftpControllerClass()
    data = c_sftp.sftpList()
    return render(request, 'sftp_list.html', {'data': data})

# 删除sftp 项
def deleteSftp(request):
    c_sftp = SftpControllerClass()
    id = c_sftp.deleteSftp(request)
    return JsonResponse(id, safe=False)

# 添加用户
def add_user(request):
    c_machine = MachineControllerClass()
    data = c_machine.getMachineSimpleListInfo()
    return render(request, 'add_user.html', {'data': data})

# 用户列表
def user_list(request):
    c_user = UserControllerClass()
    data = c_user.getUserList()
    print '1111111111:',data
    return render(request, 'user_list.html', {'data': data})

# 编辑用户
def edit_user(request):
    data = {}
    c_machine = MachineControllerClass()
    data['machine'] = c_machine.getMachineSimpleListInfo()
    c_user =UserControllerClass()
    data['user'] = c_user.getUserInfoById(request)
    return render(request, 'edit_user.html', {'data': data})

# 编辑用户接口
def editUser(request):
    c_user = UserControllerClass()
    id = c_user.updateUser(request)
    return JsonResponse(id, safe=False)

# 后台显示首页
def home(request):
    return render(request, 'home.html', {'data': 'home testdata'})

# 添加机器页面
def add_machine(request):
    return render(request, 'add_machine.html', {'data':'add_machine testdata'})

# 编辑机器页面
def edit_machine(request):
    id = request.GET.get('id')
    data = {}
    data['id'] = id
    c_machine = MachineControllerClass()
    data['envinfo'] = c_machine.getEnvInfo()
    data['data'] = c_machine.getMachineInfoById(id)
    return render(request, 'edit_machine.html', {'data':data})

# 通过id　获取　机器信息
def getMachineInfoById(request):
    c_machine = MachineControllerClass()
    return JsonResponse(c_machine.getMachineInfoById(request), safe=False)

# 机器列表页面
def machine_list(request):
    c_machine = MachineControllerClass()
    data = c_machine.getMachineListInfo()
    return render(request, 'machine_list.html', {'data':data})

# 添加环境 页面
def add_env(request):
    return render(request, 'add_env.html', {'data':'test add_env'})

# 编辑 环境页面
def edit_env(request):
    c_env = EnvControllerClass()
    data = c_env.edit_env(request)
    return render(request, 'edit_env.html', {'data': data})

# 编辑 环境
def editEnv(request):
    c_env = EnvControllerClass()
    id = c_env.updateEnv(request)
    return JsonResponse(id, safe=False)

# 检测ip 在 machine 表中是否存在
def checkip(request):
    c_machine = MachineControllerClass()
    return JsonResponse(c_machine.checkip(request), safe=False)


# 检测 项目编码
def checkProjectCode(request):
    c_project = ProjectControllerClass()
    return JsonResponse(c_project.checkProjectCode(request), safe=False)


# 根据包名、应用名，检测包名、应用名唯一
def checkAppName(request):
    c_app = AppControllerClass()
    return JsonResponse(c_app.checkAppName(request), safe=False)

# 检测用户在主机上是否已经存在
def checkUserMachineExists(request):
    c_user = UserControllerClass()
    return JsonResponse(c_user.checkUserMachineExists(request), safe=False)

# 删除用户
def deleteUser(request):
    c_user = UserControllerClass()
    return JsonResponse(c_user.deleteUser(request), safe=False)

# 检测用户连接性
def testConnect(request):
    c_user = UserControllerClass()
    return JsonResponse(c_user.testConnect(request), safe=False)









