#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
功能：任务控制
说明：根据前端获取的json数据，生成任务步骤表。根据任务步骤表步骤 逐步执行对应任务。
"""
from ..Model.taskModelClass import *
from ..Model.ftpModelClass import *
from ..Model.taskstepModelClass import *
from ..Model.projectModelClass import *
from ..Model.appModelClass import *
from ..Model.upgradestepModelClass import *
from ..Extends.sycnlocaltool import *
from ..Controllers.ftpControllerClass import *
from ..Extends import lock
from ..Model.upgradeappModelClass import *
import json

class TaskControllerClass(object):

    # 根据数据 判断包含应用、数据库应用的三种情况，只有应用返回 app,只有DB返回 db, 应用和DB则返回 app_db
    def isIncludeAppDb(self, data):
        has_app = 'false'
        has_db = 'false'
        for i in range(len(data['project'])):
            if data['project'][i].has_key('app'):
                has_app = 'true'
                break
            if data['project'][i].has_key('db'):
                has_db = 'true'
                break
        if has_app == 'true' and has_db == 'true':
            return 'app_db'
        elif has_app == 'true' and has_db == 'false':
            return 'app'
        elif has_app == 'false' and has_db == 'true':
            return 'db'
        else:
            return ''

    # 将前端返回的json 数据解析返回
    def getFontJsonDataToDic(self, request):
        # print json.loads(request.body)
        # return json.loads(request.body)
        # request.session.get('project_name')
        # request.session.get('apps')
        # request.session.get()
        # request.session.get()
        # request.session.get()
        data = json.loads(request.body)
        # data = {
        #     'env_type' :request.POST.get('envtype'),
        #     'project' :[{
        #         'name' : request.POST.get('project[0][name]'),
        #         'version' : request.POST.get('project[0][version]'),
        #         'app': request.POST.get('project[0][app][]'),
        #         #'DB' : ['10.1.1.100-test', '10.1.1.101-test1'] # 可以暂时不考虑DB,此处数据可以省略
        #     }#,{
        #      #   'name' : 'ALS',
        #      #   'version' : 'v101001',
        #      #   'app': ['alsapp.war'],
        #      #   #'DB' : ['10.1.1.100-test', '10.1.1.101-test1'] # 可以暂时不考虑DB,此处数据可以省略
        #     #}]
        #     ]
        # }
        appmode = upgradeappModelClass()
        applist=[]
        for war in data['project'][0]['app']:
            appname = appmode.getnamebypkgname(war)
            applist.append(appname)
        request.session['apps']= applist
        return data

    # 校验前端数据 和 后端数据一致性,不一致返回 False ，一致返回True
    def checkFontData(self, data):
        # print "data is ,,,,::", data
        retstr = self.isIncludeAppDb(data)
        check_flag = True
        if retstr == 'app':
            for i in range(len(data['project'])):
                for j in range(len(data['project'][i]['app'])):
                    warname = str(data['project'][i]['app'][j]).strip()
                    appname = AppModelClass().getAppNameByWarName(warname)
                    if appname == '':
                        print "Can not know war name : [ " + warname + " ]"
                        check_flag = False
                        continue
            return check_flag
        elif retstr == 'db':
            print "new function is deloping "
            return False
        elif retstr == 'app_db':
            print "new function is deloping "
            return False
        else:
            print "please check data is right ."
            return False

    # 根据数据 生成 task_step 表数据
    def writeTaskStepData(self, request):
        data = self.getFontJsonDataToDic(request)
        if self.checkFontData(data) == False: # 检测前端数据正确性
            return False
        app_db_str = self.isIncludeAppDb(data)
        if app_db_str == 'app':
            m_task = TaskModelClass()
            id = m_task.createTaskTaskData() # 创建任务,返回ID
            m_taskstep = TaskstepModelClass()
            print lock.lock
            if lock.lock==1:
                lock.lock=2
                ret = m_taskstep.addDataToTaskStepByStr(id, app_db_str)
                print "ret_listis ,,;:", ret
                lock.lock=1
            request.session['taskid'] = id
            return self.saveJsonDataToLocalFile(data, id) # 保存到文件中
            # return id
        elif app_db_str == 'db':
            print "new function is deloping "
            return False
        elif app_db_str == 'app_db':
            print "new function is deloping "
            return False
        else:
            print "please check data is right ."
            return False

    # 由于后面需要用到对应的json 数据，所以认为创建完成后，将json 存储在本地文件中
    def saveJsonDataToLocalFile(self, data, taskid):
        m_task = TaskModelClass()
        dir_name = m_task.getTaskDirNameById(taskid)
        timedir = os.path.dirname(os.path.abspath(__file__)) + '/../../tasks/' + dir_name
        cmds = [['mkdir', '-p', timedir]]
        if execShellCommand(*cmds) == False: # 创建目录
            return False
        local_file = os.path.dirname(os.path.abspath(__file__)) + '/../../tasks/' + dir_name + '/task.json'
        try:
            f = open(local_file, "w")
            f.write(json.dumps(data, ensure_ascii=False) + "\n")  # 保存前，需要将jsonStr序列化为python相对的数据类型，去掉最后的换行符
            f.close()
        except Exception, e:
            print "[ERROR] saveJsonDataToLocalFile failed  ======"
            return False
        return True

    # 从文件中读取 json 数据
    def readJsonFromLocalFile(self, taskid):
        m_task = TaskModelClass()
        dir_name = m_task.getTaskDirNameById(taskid)
        local_json_file = os.path.dirname(os.path.abspath(__file__)) + '/../../tasks/' + dir_name + '/task.json'
        for eachLine in open(local_json_file, "r"):
            jsonData = json.loads(eachLine);  # 反序列化，得到json格式数据
        # print "result888888888888888:", json.dumps(jsonData, indent=4)
        return jsonData

    # 根据字典数据 获取 应用名、user 、ip 数据
    def getdata2return2(self, **data):
        ret_list = []
        taskmdcl = TaskModelClass()
        for i in range(len(data['project'])):
            env_name = data['envtype']
            project_name = data['project'][i]['name']
            project_ver = data['project'][i]['version']
            for j in range(len(data['project'][i]['app'])):
                war_name = str(data['project'][i]['app'][j]).strip()
                app_name = taskmdcl.getAppNameByWarName(war_name) # 通过 包名 获取 应用名
                if app_name != '':
                    paralist = taskmdcl.getdata1(app_name,env_name)  # 应用名、user、ip
                    # print "paralist22222222 :",paralist
                    if len(paralist) != 0:
                        for para in paralist:
                            ret_list.append([para, project_name, project_ver])
        return ret_list

    # 执行任务总入口函数
    def clickCommand(self, request):
        taskid = request.POST.get('taskid')
        stepname = request.POST.get('step_name')
        tm=TaskstepModelClass()
        ups=upgradestepModeClass()
        if taskid == '':
            print "======  taskid is null  ========"
            return False
        stepid = ups.getidbyname(stepname)
        if stepname == 'upload':
            ### 这里需要变更状态到 数据库表
            tm.updatestep(taskid=taskid,stepid=stepid,status=1)
            ## 这是开始执行 文件下载和分发步骤

            if self.downLoadFiles(taskid) == False:
                print '11111上传下载失败'
                tm.updatestep(taskid=taskid, stepid=stepid, status=-1)

                return False
            if self.runUploadFilesToClients(taskid) == 'false':
                print '222222上传下载失败'
                tm.updatestep(taskid=taskid, stepid=stepid, status=-1)

                return False
            print '上传下载完成'
            tm.updatestep(taskid=taskid, stepid=stepid, status=2)
            data = tm.getnextstopstatus(taskid, stepid)
            status = int(data[0])
            nextstepname = ups.getnamebyid(data[1])
            # print status,nextstepname
            # status = tm.getIsStopedStatus(taskid,stepid)
            while status == 0:
                stepid = ups.getidbyname(nextstepname)
                tm.updatestep(taskid=taskid, stepid=stepid, status=1)
                result = self.runStep(taskid, nextstepname)
                data = tm.getnextstopstatus(taskid, stepid)
                status = int(data[0])
                nextstepname = ups.getnamebyid(data[1])
                if result == False:
                    stepremark = ups.getremark(stepid)

                    print '{0} 失败'.format(stepremark)

                    tm.updatestep(taskid=taskid, stepid=stepid, status=-1)
                    break
                stepremark = ups.getremark(stepid)
                print '{0} 完成'.format(stepremark)
                tm.updatestep(taskid=taskid, stepid=stepid, status=2)
        else:
            # print taskid,stepid
            # data = tm.getnextstopstatus(taskid, stepid)
            # status = int(data[0])
            # nextstepname = ups.getnamebyid(data[1])
            # print status,nextstepname
            status = tm.getIsStopedStatus(taskid,stepid)
            while status == 0:
                stepid = ups.getidbyname(stepname)
                tm.updatestep(taskid=taskid, stepid=stepid, status=1)
                result = self.runStep(taskid, stepname)
                data = tm.getnextstopstatus(taskid, stepid)
                status = int(data[0])
                stepname = ups.getnamebyid(data[1])
                if result == False:
                    stepremark = ups.getremark(stepid)

                    print '{0} 失败'.format(stepremark)

                    tm.updatestep(taskid=taskid, stepid=stepid, status=-1)
                    break
                stepremark = ups.getremark(stepid)
                print '{0} 完成'.format(stepremark)
                tm.updatestep(taskid=taskid, stepid=stepid, status=2)
                # status = tm.getIsStopedStatus(taskid, stepid)

        return True

    # 下载 sftp 上的包
    def downLoadFiles(self, taskid):
        data = self.readJsonFromLocalFile(taskid) # 从本地文件加载 json
        env_type = data['envtype']
        project_list = []
        for i in range(len(data['project'])):
            project_list.append([data['project'][i]['name'], data['project'][i]['version']])
        m_ftp = FtpModelClass()
        m_project = ProjectModelClass()
        c_ftp = FtpControllerClass()
        for eachp_no_ver in project_list:  # 遍历[['HCS', 'v001001'],['ALS', 'V110110']]
            eachproject_no = eachp_no_ver[0]
            eachproject_ver = eachp_no_ver[1]

            dic = m_ftp.getProjectEnvConnectsInfo(env_type,eachproject_no) # 获取项目的连接信息
            print "dic111111:", dic
            appnamelist = []
            for app in data['project'][0]['app']:
                appname = m_project.getAppNameBywar(app)  # 获取应用列表
                appnamelist.append(appname)
            print "appnamelist 888888 :", appnamelist
            for eachapp in appnamelist:
                ret = c_ftp.downLoadPkgs(eachproject_no, eachproject_ver, eachapp, taskid, **dic)  # 版本号、应用名称、任务ID、连接信息字典
                if ret == False:
                    return ret
        print  "======= download all files successed   ========"
        return True


    # 将文件同步到 每台客户端
    def runUploadFilesToClients(self, taskid):
        data1 = self.readJsonFromLocalFile(taskid) # 读取本地的json 数据
        m_task = TaskModelClass()
        dirname = m_task.getTaskDirNameById(taskid)
        retlist = self.getdata2return2(**data1)
        #print 'data1:',data1,'retlist:',retlist
        # print "retlist is 888888888:", retlist
        ret = sycnlocaltool.syncloacl(retlist, dirname)
        return ret

    # 运行对应的步骤，除了上传文件的步骤
    def runStep(self, taskid, step):
        print "[INFO] is running step: [ " + str(step) + " ] "

        data1 = self.readJsonFromLocalFile(taskid)    # 读取本地的json 数据
        m_task = TaskModelClass()
        dirname = m_task.getTaskDirNameById(taskid)
        retlist = self.getdata2return2(**data1)

        ret = sycnlocaltool.runStep(retlist, dirname, step)  # 运行远程端脚本
        if ret == 'false':
            return False
        ###### 是否执行下一步，如果执行，调用下一个步骤 ####
        m_taskstep = TaskstepModelClass()
        if m_taskstep.getIsStopedStatus2(taskid, step) == '1':
            print "[INFO] excute step : [ " + str(step) + " ] stoped ."
            return True
        else:
            retdata = self.getNextStepName(taskid, step)
            if retdata == '':
                return False
            elif retdata == 'end':
                return True
            # else:
            #     return self.runStep(taskid, retdata)
        return True

    # 更改步骤 is_stoped 的状态
    def clickStepStopStart(self, request):
        taskid = request.POST.get('taskid')
        stepname = request.POST.get('stepname')
        m_step = TaskstepModelClass()
        return m_step.changeIsStopedValue(taskid, stepname)

    # 根据当前步骤 获取下一个步骤名称 返回下一个步骤名称
    def getNextStepName(self, taskid, stepname):
        m_taskstep = TaskstepModelClass()
        all_step = m_taskstep.getTaskStepSequence(taskid)
        if all_step == '':
            return ''
        for i in range(len(all_step)):
            if all_step[i][2] == stepname:
                if i + 1 >= len(all_step):
                    print "[INFO] this step : [ " + str(stepname) + " ] is last step ."
                    return 'end'
                else:
                    return all_step[i+1][2]


