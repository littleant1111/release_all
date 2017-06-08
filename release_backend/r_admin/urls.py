#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^index/$',  index, name='index'),
    url(r'^login/$',  login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^password_change/$', password_change,name='password_change'),
    url(r'^password_change_done/$', password_change_done, name='password_change_done'),

    ## 页面映射
    url(r'^home/$', home, name='home'),
    url(r'^add_machine/$', add_machine, name='add_machine'),
    url(r'^machine_list/$', machine_list, name='machine_list'),
    url(r'^add_project/$', add_project, name='add_project'),
    url(r'^project_list/$', project_list, name='project_list'),
    url(r'^add_env/$', add_env, name='add_env'),
    url(r'^env_list/$', env_list, name='env_list'),
    url(r'^add_app/$', add_app, name='add_app'),
    url(r'^app_list/$', app_list, name='app_list'),
    url(r'^add_sftp/$', add_sftp, name='add_sftp'),
    url(r'^sftp_list/$', sftp_list, name='sftp_list'),
    url(r'^add_user/$', add_user, name='add_user'),
    url(r'^user_list/$', user_list, name='user_list'),


    url(r'^getEnvInfo/$', getEnvInfo, name='getEnvInfo'),
    url(r'^addMachine/$', addMachine, name='addMachine'),
    url(r'^deleteMachine/$', deleteMachine, name='deleteMachine'),
    url(r'^addProject/$', addProject, name='addProject'),
    url(r'^deleteProject/$', deleteProject, name='deleteProject'),
    url(r'^getProjectList/$', getProjectList, name='getProjectList'),
    url(r'^addEnv/$', addEnv, name='addEnv'),
    url(r'^deleteEnv/$', deleteEnv, name='deleteEnv'),
    url(r'^addApp/$', addApp, name='addApp'),
    url(r'^deleteApp/$', deleteApp, name='deleteApp'),
    url(r'^addUser/$', addUser, name='addUser'),
    url(r'^addSftp/$', addSftp, name='addSftp'),
    url(r'^deleteSftp/$', deleteSftp, name='deleteSftp'),

    # 前后端交互
    url(r'^checkip/$', checkip, name='checkip'),
    url(r'^checkProjectCode/$', checkProjectCode, name='checkProjectCode'),
    url(r'^checkAppName/$', checkAppName, name='checkAppName'),
    url(r'^checkUserMachineExists/$', checkUserMachineExists, name='checkUserMachineExists'),
    url(r'^deleteUser/$', deleteUser, name='deleteUser'),

    ## 编辑 机器
    url(r'^edit_machine/$', edit_machine, name='edit_machine'),
    url(r'^getMachineInfoById/$', getMachineInfoById, name='getMachineInfoById'),
    url(r'^editMachine/$', editMachine, name='editMachine'),

    # 编辑 项目
    url(r'^edit_project/$', edit_project, name='edit_project'),
    url(r'^editProject/$', editProject, name='editProject'),

    #编辑 env
    url(r'^edit_env/$', edit_env, name='edit_env'),
    url(r'^editEnv/$', editEnv, name='editEnv'),

    #编辑应用
    url(r'^edit_app/$', edit_app, name='edit_app'),
    url(r'^editApp/$', editApp, name='editApp'),

    # 编辑用户
    url(r'^edit_user/$', edit_user, name='edit_user'),
    url(r'^editUser/$', editUser, name='editUser'),
    url(r'^testConnect/$', testConnect, name='testConnect'),


]