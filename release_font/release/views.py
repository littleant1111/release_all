#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from Controllers.loginControllerClass import *
from Controllers.projectControllerClass import *
from Controllers.ftpControllerClass import *
from Controllers.taskControllerClass import *
from Extends.paramikoTool import *
from Extends.sycnlocaltool import *
from models import *
from Model.taskModelClass import *
from Model.ftpModelClass import *
from Model.projectModelClass import *
from Model.quanxianModelClass import *

from Model.upgradeappModelClass import *
from Model.taskstepModelClass import *
from django.core import serializers
from Extends.getLogTool import *
import os


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


# 根据projectid 获取应用名称
def getAppNameByProjectId(request):
    c_project = ProjectControllerClass()
    data = c_project.getAppNameByProjectId(1)
    return JsonResponse(data, safe=False)

# 获取 sftp/ftp 端文件
def getRemoteFiles(request):
    c_ftp = FtpControllerClass()
    return JsonResponse(c_ftp.getAppPkgNameByProjectName(), safe=False)

# 获取所有项目信息
def getProjectInfo(request):
    c_project = ProjectControllerClass()
    return JsonResponse(c_project.getProjectInfo(), safe=False)

# 获取所有环境类型信息
def getEnvType(request):
    pass


# 任务创建完成,如果创建成功后，页面跳转到发布页面
def taskBegin(request):
    bodydata = json.loads(request.body)
    print 'adfasf7',bodydata
    if bodydata.has_key('taskid'):
        request.session['apps']= bodydata['apps']
        request.session['taskid']=bodydata['taskid']
        request.session['env_child'] = bodydata['envtype']
        request.session['project_name']=bodydata['project'][0]['name']
        return JsonResponse('true', safe=False)
    c_task = TaskControllerClass()
    data = c_task.writeTaskStepData(request)
    # request.session['taskid'] = 1000
    if data == True:
        return JsonResponse('true', safe=False)
    else:
        return JsonResponse('false', safe=False)

# 发布页面 表单填写页面
def release(request):
    if request.COOKIES.get('sessionid') is None:
        return redirect('/release/index/')
    return render(request, 'release.html')

# 发布页面 详情页面
def detail(request):
    taskid = request.session.get('taskid')
    # print 'tttttttttttttttttttttttid:',taskid
    return render(request, 'detail.html', {'taskid': taskid})

# 更改红绿灯
def clickRedGreen(request):
    '''
    type : 'POST',
　　url : '/release/clickRedGreen/',
　　data:{
        'is_stop': is_stop
    },
    '''
    is_stop = request.POST.get('is_stop')
    stepid = request.POST.get('stepid')

    # is_stop = request.POST.get('step')
    # is_stop = request.POST.get('is_stop')
    # print 'is_stopis :', is_stop
    if is_stop == '1':
        taskstepmode = TaskstepModelClass()
        taskstepmode.updateisstop(0, stepid)
        return JsonResponse('0', safe=False)
    else:
        taskstepmode = TaskstepModelClass()
        taskstepmode.updateisstop(1, stepid)
        return JsonResponse('1', safe=False)




# 前端点击当前步骤的红绿点，ajax 操作,更改task_step is_stoped 值
def clickStepStopStart(request):
    c_task = TaskControllerClass()
    if c_task.clickStepStopStart(request) == False:
        return JsonResponse('failed', safe=False)
    else:
        return JsonResponse('success', safe=False)

# 根据projectid 获取应用名称
def getAppNameByProjectId(request):
    c_project = ProjectControllerClass()
    data = c_project.getAppNameByProjectId(1)
    return JsonResponse(data, safe=False)

# 获取 sftp/ftp 端文件
def getRemoteFiles(request):
    c_ftp = FtpControllerClass()
    return JsonResponse(c_ftp.getAppPkgNameByProjectName(), safe=False)

# 获取所有项目信息
def getProjectInfo(request):
    c_project = ProjectControllerClass()
    return JsonResponse(c_project.getProjectInfo(), safe=False)

# 发布历史页面
def history(request):
    if request.COOKIES.get('sessionid') is None:
        return redirect('/release/index/')
    return render(request, 'history.html')

# 配置页面
def config(request):
    if request.COOKIES.get('sessionid')==None:
        return redirect('/release/index/')
    return render(request, 'config.html')

# # 根据发布阶段，获取发布的所有环境类型，传入
# def getEnvByStep(request):
#     step_type = request.POST.get('env_step')
#     if step_type == 'sit':
#         data = ['sit1', 'sit2', 'sit3', 'sit4']
#     elif step_type == 'uat':
#         data = ['uat1', 'uat2', 'uat3']
#     elif step_type == 'pre':
#         data = ['pre1', 'pre2']
#     elif step_type == 'prd':
#         data = ['prd1', 'prd2']
#     return JsonResponse(data, safe=False)

# # 根据发布环境类型，获取项目名称和系统编码返回
# def getSystemInfo(request):
#     env_type = request.POST.get('env')
#     if env_type == 'sit1' or  env_type == 'sit2' or env_type == 'sit3' or env_type == 'sit4':
#         data = [('蜂巢系统','HCS'),('安硕核心', 'ALS')]
#     elif env_type == 'uat1' or env_type == 'uat2' or env_type == 'uat3':
#         data = [('安硕核心', 'ALS')]
#     elif env_type == 'pre1' or env_type == 'pre2':
#         data = [('蜂巢系统', 'HCS')]
#     elif env_type == 'prd1' or env_type == 'prd2':
#         data = [('xxx系统', 'xxx')]
#     return JsonResponse(data, safe=False)

# # 根据环境类型、系统编码 获取版本号，列表返回
# def getVersionByEnvAndSysCode(request):
#     env = request.POST.get('env')
#     code = request.POST.get('code')
#     if code == 'HCS':
#         data = ['v100100x', 'v100101x', 'v100102x', 'v100103x', 'v100104x', 'v100105x']
#     if code == 'ALS':
#         data = ['v100100Y', 'v100101Y', 'v100102Y', 'v100103Y']
#
#     return JsonResponse(data, safe=False)

# # 根据 环境类型、系统编码、和版本，获取所有应用的包名
# def getPkgName(request):
#     env = request.POST.get('env')
#     code = request.POST.get('code')
#     version = request.POST.get('version')
#     if code == 'HCS':
#         data = ['a.war', 'b.war', 'c.war', 'd.war', 'e.war', 'f.war']
#     if code == 'ALS':
#         data = ['1.war', '2.war', '3.war', '4.war', '5.war', '6.war']
#     else:
#         data = ['abc.war', 'xxx.war', 'yyy.war']
#     return JsonResponse(data, safe=False)



# # 运行所有任务，前端只需要传递 json 过来即可完成所有步骤
# def runAll(request):
#
#     ###### 写入表数据 ################
#     c_task = TaskControllerClass()
#     data = c_task.writeTaskStepData(request)
#     ###### 写入表数据 结束  ################
#
#     ####  测试下载  ############
#     m_ftp = FtpModelClass()
#     dic = m_ftp.getProjectEnvConnectsInfo('HCS', 'sit')
#     print "dic111111:", dic
#     m_project = ProjectModelClass()
#     appnamelist = m_project.getAppNameByProjectNo('HCS')
#     print "appnamelist 888888 :", appnamelist
#     # return JsonResponse('download successed', safe=False)
#     c_ftp = FtpControllerClass()
#     for eachapp in appnamelist:
#         ret = c_ftp.downLoadPkgs('v100100', eachapp, '26', **dic) # 版本号、应用名称、任务ID、连接信息字典
#         if ret == False:
#             return JsonResponse('download '+ str(eachapp) + 'failed', safe=False)
#     # return JsonResponse('download successed', safe=False)
#     print  "======= download all files successed   ========"
#     ####  测试end  ############
#
#     ### 测试同步文件到远程 #########
#     c_task = TaskControllerClass()
#     if c_task.runUploadFilesToClients(request) == 'false':
#         return JsonResponse('sync files failed ', safe=False)
#     # else:
#     #     return JsonResponse('sync files successed  ', safe=False)
#     print  "======= sync all files to clients successed   ========"
#     ### 测试同步文件到远程 结束 #########
#
#     ###### 执行步骤  #############
#     if c_task.runStep(request) == 'false':
#         return JsonResponse('run step failed !', safe=False)
#     print  "======= run step successed   ========"
#     return JsonResponse('run step successed !', safe=False)


##############################################
def test(request):
    m_task_step = TaskstepModelClass()
    # data = m_task_step.getIsStopedStatus2('26','check')
    # print "status is ::",data
    c_task = TaskControllerClass()
    data = c_task.getNextStepName('52', 'rollback')
    print "data list is :", data
    return JsonResponse('test !', safe=False)

# 同步文件到远程，并加上执行权限
def syncFiles(request):
    pass
    # data1 = {
    #     'env_type': 'sit',
    #     'project': [{
    #         'name': 'HCS',
    #         'version': 'v001001',
    #         'app': ['LoginSYS.war', 'beehive.war', 'testapp.war'],
    #     }, {
    #         'name': 'ALS',
    #         'version': 'v101001',
    #         'app': ['alsapp.war'],
    #     }]
    # }
    # dirname = '201701192046_1484830009'
    # taskcc = TaskControllerClass()
    # retlist = taskcc.getdata2return2(**data1)
    # print "retlist is 888888888:", retlist
    # # return JsonResponse(retlist, safe=False)
    #
    # ret = sycnlocaltool.syncloacl(retlist, dirname)
    # # ret = sycnlocaltool.runStep(retlist, dirname, 'check')
    # if ret == 'false':
    #     return JsonResponse('exec failed .', safe=False)
    # else:
    #     return JsonResponse('syncFiles ok', safe=False)

# 测试前端的json
def testjson(request):
    received_json_data = json.loads(request.body)
    # print "request,,, ret is :", received_json_data

    return JsonResponse('ok', safe=False)

def test2(request):
    m_task = TaskModelClass()
    data = m_task.getAppNameByWarName('beehive.war')
    print data
    return JsonResponse(data, safe=False)

def getEnvByStep(request):
    step_type = request.POST.get('env_step')
    if step_type == 'sit':
        e = env.objects.get(name='sit')
        data = list(e.env_child_set.values('envchild_name'))
    elif step_type == 'uat':
        e = env.objects.get(name='uat')
        data = list(e.env_child_set.values('envchild_name'))
    elif step_type == 'pre':
        e = env.objects.get(name='pre')
        data = list(e.env_child_set.values('envchild_name'))
    elif step_type == 'prd':
        e = env.objects.get(name='prd')
        data = list(e.env_child_set.values('envchild_name'))
    ret_data=[]
    username = request.user
    qmd=quanxianModelClass()
    envlist = list(qmd.getenvnamebyuser(username))
    print 'envlist',envlist
    print data
    for da in data:
        if da['envchild_name'] in envlist:
            ret_data.append(da['envchild_name'])
    request.session['env'] = step_type
    return JsonResponse(ret_data, safe=False)

# 根据发布环境类型，获取项目名称和系统编码返回
def getSystemInfo(request):
    env_type = request.POST.get('env')
    print env_type
    e = env_child.objects.get(envchild_name=env_type)
    data = list(e.project_set.values('name','remark'))
    request.session['env_child'] = env_type
    ret_list=[]
    for da in data:
        lis=[]
        lis.append(da['remark'])
        lis.append(da['name'])
        ret_list.append(lis)
    return JsonResponse(ret_list, safe=False)

# 根据环境类型、系统编码 获取版本号，列表返回
def getVersionByEnvAndSysCode(request):
    env = request.POST.get('env')
    code = request.POST.get('code')
    ftp=FtpControllerClass()
    data = ftp.getVersionByProjectName(env,code)
    request.session['project_code'] = code
    request.session['project_name'] = project.objects.get(name = code ).remark

    return JsonResponse(data, safe=False)

# 根据 环境类型、系统编码、和版本，获取所有应用的包名
def getPkgName(request):
    env = request.POST.get('env')
    code = request.POST.get('code')
    version = request.POST.get('version')
    ftp=FtpControllerClass()
    data = ftp.getAppPkgNameByProjectName(env,code,version)
    request.session['env_child'] = env
    appmode = upgradeappModelClass()
    wars = []
    for war in data:
        appname = appmode.getnamebypkgname(war)
        if appname !='':
            wars.append(war)
    request.session['appswar'] = wars

    request.session['version'] = version
    return JsonResponse(data, safe=False)



    #根据应用名获取发布机ip列表
def getIpaddresses(request):
    appname=request.POST.get('app')
    env_child=request.session.get('env_child')
    appmode = upgradeappModelClass()
    data = appmode.getipbyname(appname,env_child)
    ret_data = []
    for da in data:
        ret_data.append(da[0])
    return JsonResponse(ret_data, safe=False)

def getRemoteLog(request):
    """taskid:385
project_code:HCS
app:LoginSYS
ip:10.80.7.78
step_id:2084"""
    ip = request.POST.get('ip')
    app = request.POST.get('app')
    appmode=AppModelClass()
    dic = appmode.getuserByappip(app,ip)
    print app,type(dic),type(app),dic
    dic['app'] = app
    # stepid = '2107'

    stepid = request.POST.get('step_id')
    taskstepmode=TaskstepModelClass()
    stepname = taskstepmode.getnamebytaskid(stepid)
    dic['stepname'] = stepname
    if stepname=='upload':
        return JsonResponse('暂时无法获取！', safe=False)
    taskid = request.POST.get('taskid')

    taskmode = TaskModelClass()
    taskdir = taskmode.getTaskDirNameById(taskid)
    dic['taskdir'] = taskdir
    logtoll = GetLogTool(**dic)
    data = logtoll.getlogallrow()

    # getlogtool = GetLogTool(*dic)
    # self.username = dict['username']
    # self.password = dict['password']
    # self.log_file = dict['log_file']
    # self.rownum = dict['rownum']
    # self.port = dict['port']
    # taskid='201702151527_1487143650'
    # app='LoginSYS'
    # ip='10.80.7.79'
    # stepname='checkapp'

    return JsonResponse(data, safe=False)


# 前端定时任务查询任务状态，步骤信息
def getTaskInfo(request):
    taskid=request.POST.get('taskid')
    taskstepmode=TaskstepModelClass()
    data=taskstepmode.getidstatusbytaskid(taskid)

    log = os.popen('tail -n 50 nohup.out').read()
    dic = {}
    dic['task'] = data
    try:
        dic['log'] = unicode(log)
    except Exception,e:
        dic['log']=''

    return JsonResponse(dic, safe=False)

    ## 发布详情页面需要数据 ##
def detail(request):

    data = {}
    data['taskid'] = str(request.session.get('taskid'))
    data['env'] = request.session.get('env_child')
    data['project_code'] = request.session.get('project_code')
    data['project_name'] = request.session.get('project_name')
    data['version'] = request.session.get('version')
    data['apps'] = request.session.get('apps')
    stepmodel = TaskstepModelClass()
    data['steps'] = stepmodel.getdetailbytaskid(data['taskid'])
    print 'afdafsffdfafadsfdfdasdfaafdfdfdas',data
    return render(request, 'detail.html', {'data':data})

# 前端点击执行任务按钮 taskid, stepname
def clickCommand(request):
    print request.body
    taskstepmode = TaskstepModelClass()
    ret_dic = taskstepmode.getstatuisstopbyid(request.POST.get('step_id'))
    if ret_dic['result'] == 'false':
        return JsonResponse(ret_dic, safe=False)
    env,project_code,version,apps,taskid=request.session.get('env_child'), \
                                         request.session.get('project_code'), request.session.get('version'),\
                                         ','.join(request.session.get('apps')), request.POST.get('taskid')
    param=[env,project_code,version,apps,str(taskid)]

    taskmode = TaskModelClass()
    print param

    taskmode.updatetaskstart(param)
    c_task = TaskControllerClass()
    ret = c_task.clickCommand(request)
    create_time,end_time,states=taskstepmode.getmintimebyid(taskid),taskstepmode.getmaxtimebyid(taskid),taskstepmode.getstatus(taskid)
    print create_time,end_time,states
    format = '%Y-%m-%d %H:%M:%S'
    if end_time==0:
        end_time = time.time()
    create_time = time.strftime(format, time.localtime(int(create_time)))
    end_time = time.strftime(format, time.localtime(int(end_time)))
    print create_time,end_time,states

    if int(states) == 0:
        result = '未开始'
    elif int(states) == 1:
        result = '运行中'
    elif int(states) == -1:
        result = '异常'
    elif int(states) == 2:
        result = '完成'
    print create_time,end_time,states

    param2=[create_time,end_time,result,str(taskid)]
    print param2
    taskmode.updatetaskend(param2)

    if ret == True:
        return JsonResponse({'result':'true','msg':''}, safe=False)
    else:
        return JsonResponse({'result':'false','msg':'error'}, safe=False)




def gethistory(request):

    taskmode = TaskModelClass()
    historylist = taskmode.gethistoryall()
    retdic={}
    datalist = []
    for history in historylist:
        dic = {}
        dic['id'], dic['env'],dic['project_code'], \
        dic['version'], dic['apps'], dic['create_time'], dic['end_time'], dic['states'] =history[0],history[1],\
                                                                            history[2],history[3],history[4],history[5],history[6],history[7]

        datalist.append(dic)

    retdic['data'] = datalist


    return JsonResponse(retdic,safe=False)


def bsdetail(request):
    print 'start',request.user
    envchild_name=request.POST.get('envchild_name')
    retdic={}
    retdic['envchild']=list(env_child.objects.values_list('envchild_name', flat=True))

    if envchild_name == None:
        print retdic
        taskmode = TaskModelClass()
        bsdetaillist = taskmode.getbsdetail(envchild_name)
        print envchild_name
        datalist = []
        for bsdetail in bsdetaillist:
            dic = {}
            dic['envchild_name'], dic['project_name'],dic['app_name'], \
            dic['ip'], dic['user'], dic['appdir']=bsdetail[0],bsdetail[1],bsdetail[2],bsdetail[3],bsdetail[4],bsdetail[5]
            datalist.append(dic)
        print datalist
        retdic['data'] = datalist
        return render(request, 'bsdetail.html', retdic)
    else:
        taskmode = TaskModelClass()
        bsdetaillist = taskmode.getbsdetail(envchild_name)
        print envchild_name
        datalist = []
        for bsdetail in bsdetaillist:
            dic = {}
            dic['envchild_name'], dic['project_name'],dic['app_name'], \
            dic['ip'], dic['user'], dic['appdir']=bsdetail[0],bsdetail[1],bsdetail[2],bsdetail[3],bsdetail[4],bsdetail[5]
            datalist.append(dic)
        print datalist
        retdic['data'] = datalist
    return render(request,'bsdetail.html',retdic)

def getbsdetail(request):

    envchild_name=request.POST.get('envchild_name')
    taskmode = TaskModelClass()
    bsdetaillist = taskmode.getbsdetail(envchild_name)
    print envchild_name
    retdic={}
    datalist = []
    for bsdetail in bsdetaillist:
        dic = {}
        dic['envchild_name'], dic['project_name'],dic['app_name'], \
        dic['ip'], dic['user'], dic['appdir']=bsdetail[0],bsdetail[1],bsdetail[2],bsdetail[3],bsdetail[4],bsdetail[5]
        datalist.append(dic)
    print datalist
    retdic['data'] = datalist
    return JsonResponse(retdic,safe=False)



