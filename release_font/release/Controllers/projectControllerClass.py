#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Model.projectModelClass import *


class ProjectControllerClass(object):

    # 根据projectid 获取应用名称
    def getAppNameByProjectId(self, id):
        m_project = ProjectModelClass()
        return m_project.getAppNameByProjectId(id)

    # 获取所有项目信息
    def getProjectInfo(self):
        m_project = ProjectModelClass()
        return m_project.getProjectInfo()