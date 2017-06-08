#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Model.machineModelClass import *
from ..Model.envModelClass import *


class MachineControllerClass(object):

    # 获取环境信息
    def getEnvInfo(self):
        m_env = EnvModelClass()
        return m_env.getEnvInfo()

    # 添加机器信息
    def addMachineInfo(self, request):
        data = {}
        data['name'] = request.POST.get('name')
        data['hostname'] = request.POST.get('host')
        data['ip'] = request.POST.get('ip')
        data['is_vm'] = request.POST.get('vm')
        data['cpuinfo'] = request.POST.get('cpu')
        data['memoryinfo'] = request.POST.get('memory')
        data['env'] = request.POST.get('env')
        m_Machine = MachineModelClass()
        id = m_Machine.addMachineInfo(data)
        if id != '':
            lst = [id,data['env']]
            m_env = EnvModelClass()
            n_id = m_env.addDataEnvMachine(lst)
            if n_id != '':
                return n_id
            else:
                return ''
        else:
            return ''

    # 获取机器简要 列表数据
    def getMachineSimpleListInfo(self):
        m_machine = MachineModelClass()
        return m_machine.getMachineSimpleListInfo()

    # 获取机器列表数据
    def getMachineListInfo(self):
        m_machine = MachineModelClass()
        return m_machine.getMachineListInfo()

    # 删除机器
    def deleteMachine(self, request):
        id = request.POST.get('id')
        m_machine = MachineModelClass()
        r_id = m_machine.deleteEnvMachine(id)
        if r_id != '':
            return m_machine.deleteMachine(id)
        else:
            return ''

    # 检测ip 是否存在
    def checkip(self, request):
        ip = request.POST.get('ip')
        m_machine = MachineModelClass()
        rid = m_machine.checkip(ip)
        if rid != '': # 存在
            return False
        else:
            return True

    # 通过id 获取机器对应信息
    def getMachineInfoById(self, id):
        # id = request.GET.get('id')
        m_machine = MachineModelClass()
        return m_machine.getMachineInfoById(id)

    # 通过id 等信息修改对应信息
    def updateMachine(self, request):
        data = {}
        data['id'] = request.POST.get('id')
        data['name'] = request.POST.get('name')
        data['hostname'] = request.POST.get('host')
        data['ip'] = request.POST.get('ip')
        data['is_vm'] = request.POST.get('vm')
        data['cpuinfo'] = request.POST.get('cpu')
        data['memoryinfo'] = request.POST.get('memory')
        data['env'] = request.POST.get('env')
        m_machine = MachineModelClass()
        if m_machine.updateMachine(data) == True:
            m_env = EnvModelClass()
            if m_env.updateDataEnvMachine(data['id'], data['env']) == True:
                return 'true'
            else:
                return ''
        else:
            return ''



















