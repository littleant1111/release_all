#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Model.projectModelClass import *
import json

class ProjectControllerClass(object):

    # 根据projectid 获取应用名称
    def getAppNameByProjectId(self, id):
        m_project = ProjectModelClass()
        return m_project.getAppNameByProjectId(id)

    # 获取所有项目信息
    def getProjectInfo(self):
        m_project = ProjectModelClass()
        return m_project.getProjectInfo()

    # 添加项目
    def addProject(self, request):
        data = json.loads(request.body)
        c_project = ProjectModelClass()
        id = c_project.addProject(data)
        if id != '':
            return c_project.addProjectEnv(id, data['env'])
        else:
            return ''

    # 获取所有项目信息
    def getProjectInfo2(self):
        m_project = ProjectModelClass()
        return m_project.getProjectInfo2()

    # 删除项目
    def deleteProject(self, request):
        id = request.POST.get('id')
        m_project = ProjectModelClass()
        pro_id = m_project.deleteProjectEnv(id)
        if pro_id != '':
            return m_project.deleteProject(id)
        else:
            return ''

    # 检测项目编码是否占用
    def checkProjectCode(self, request):
        code = request.POST.get('pro_code')
        m_project = ProjectModelClass()
        rid = m_project.checkProjectCode(code)
        if rid != '':
            return False
        else:
            return True

    # 通过 project_id  获取project 信息
    def getProjectInfoById(self, id):
        m_project = ProjectModelClass()
        return m_project.getProjectInfoById(id)

    # 获取项目 环境关联信息
    def getProjectEnvInfoById(self, id):
        m_project = ProjectModelClass()
        return m_project.getProjectEnvInfoById(id)

    # 保存 项目信息
    def updateProject(self, request):
        data = json.loads(request.body)
        # print 'aaaaaaaaaaaaaadata:',data
        m_project = ProjectModelClass()
        rid = m_project.updateProject(data)
        if rid != '':
            return m_project.updateProjectEnv(data['id'], data['env'])
        else:
            return ''







