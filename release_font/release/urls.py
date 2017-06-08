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
    # url(r'^getNav/$', getNav, name='getNav'),
    url(r'^getAppNameByProjectId/$', getAppNameByProjectId, name='getAppNameByProjectId'),
    url(r'^getRemoteFiles/$', getRemoteFiles, name='getRemoteFiles'),
    url(r'^getProjectInfo/$', getProjectInfo, name='getProjectInfo'),
    url(r'^taskBegin/$', taskBegin, name='taskBegin'),
    # url(r'^runAll/$', runAll, name='runAll'),
    url(r'^release/$', release, name='release'),
    url(r'^clickCommand/$', clickCommand, name='clickCommand'),


    url(r'^detail/$', detail, name='detail'),
    url(r'^history/$', history, name='history'),
    url(r'^config/$', config, name='config'),
    url(r'^bsdetail/$', bsdetail, name='bsdetail'),

    url(r'^getEnvByStep/$', getEnvByStep, name='getEnvByStep'),
    url(r'^getSystemInfo/$', getSystemInfo, name='getSystemInfo'),
    url(r'^getPkgName/$', getPkgName, name='getPkgName'),
    url(r'^clickRedGreen/$', clickRedGreen, name='clickRedGreen'),
    url(r'^getRemoteLog/$', getRemoteLog, name='getRemoteLog'),
    url(r'^getTaskInfo/$', getTaskInfo, name='getTaskInfo'),


    url(r'^test/$', test, name='test'),
    url(r'^test2$', test2, name='test2'),
    url(r'^testjson/$', testjson, name='testjson'),
    url(r'^syncFiles/$', syncFiles, name='syncFiles'),
    url(r'^getEnvByStep/$', getEnvByStep, name='getEnvByStep'),
    url(r'^getSystemInfo/$', getSystemInfo, name='getSystemInfo'),
    url(r'^getVersionByEnvAndSysCode/$', getVersionByEnvAndSysCode, name='getVersionByEnvAndSysCode'),
    url(r'^getPkgName/$', getPkgName, name='getPkgName'),
    url(r'^detail/$', detail, name='detail'),
    url(r'^getIpaddresses/$', getIpaddresses, name='getIpaddresses'),
    url(r'^getTaskInfo/$', getTaskInfo, name='getTaskInfo'),
    url(r'^gethistory/$', gethistory, name='gethistory'),
    url(r'^getbsdetail/$', getbsdetail, name='getbsdetail'),

]