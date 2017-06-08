#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import os
import subprocess
import random, base64
from hashlib import sha1
# from config.allconnect import *
import time
import datetime

# from ...config.config import *
# import ansible.runner
import json
import shutil


#### 创建目录类似于  mkdir -p dir   ########
def createDir(dir):
    logging.info("Enter createDir with successed .")
    try:
        if (os.path.exists(dir) == True):
            return True
        else:
            if(os.makedirs(dir) == True):
                return True
            else:
                logging.error("Can not create dir:[ " + dir + " ], error:[ os.makedirs ]")
                return False
    except:
        logging.error("Can not create dir:[ " + dir + " ], error:[ catch exception ]")
        return False


def listFiles(dir):
    logging.info("Enter listFiles with successed .")
    subdir = []
    retlist = []
    for item in os.listdir(os.path.abspath(dir)):
        if os.path.isfile(os.path.join(dir, item)):
            retlist.append(item)
        else:
            subdir.append(os.path.join(dir, item))

    for sdir in subdir:
        listFiles(sdir)
    return retlist

### 写字符串到文件中 ###
def writeFile(file, str='', mode='a'):
    try:
        file_object = open(file, mode)
        file_object.write(str + '\n')
        file_object.close()
        return True
    except:
        logging.error("Can not create dir:[ " + dir + " ], error:[ catch exception ]")
        return False


#### 传输脚本到远程 函数 ### 第二个参数为： [ip,user,port,password,local_dir,remote_dir]
def rsyncServerToClients(local_sync_script, *lst):
    # for i in range(len(list)):
    all_cmd_list = [] # 需要每次循环后清空
    ip = '{0}'.format(lst[0])
    user = '{0}'.format(lst[1])
    port = '{0}'.format(lst[2])
    password = '{0}'.format(lst[3])
    local_dir = '{0}'.format(lst[4])
    remote_dir = '{0}'.format(lst[5])

    sync_data_cmd = [local_sync_script, ip, user, port, password, local_dir, remote_dir]
    all_cmd_list.append(sync_data_cmd)
    # print "all_cmd_list:", all_cmd_list
    if(execShellCommand(*all_cmd_list) != True):
        print "===========  传输脚本到远程失败 =================="
        return False
    print "===========  传输脚本到远程结束 =================="
    return True

##########  执行 shell command  ####
def execShellCommand(*lst):
    # print "execShellCommand list:", lst
    for i in range(len(lst)):
        cmd_list = ''
        for j in range(len(lst[i])):
            cmd_list += '{0} '.format(lst[i][j])
        try:
            if (os.system(cmd_list) != 0):
                print "Exec command error:[ " + str(cmd_list) + " ]"
                return False
        except:
            print 'Run command error:[ ' + str(cmd_list) + ' ]'
            return False
    return True

#### 将列表值以行的形式写入到文件中 list=[['a=3', 'a'],['b=4', 'a']]#######
def writeListItemsToFile(*list):
    try:
        for i in range(len(list[0])):
            file, item, mode = list[0][i][0], str(list[0][i][1]), str(list[0][i][2])
            if(writeFile(file, item, mode) == False):
                return False
    except:
        logging.error("Can not write items to file:[ " + str(file) + " ], error:[ catch exception ]")
        return False
    return True

##### 加密函数 #######
def crypt(data, key):
    """RC4 algorithm"""
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))

    return ''.join(out)

### 加密 ###
def tencode(data, key, encode=base64.b64encode, salt_length=32):
    """RC4 encryption with random salt and final encoding"""
    salt = ''
    for n in range(salt_length):
        salt += chr(random.randrange(256))
    data = salt + crypt(data, sha1(key + salt).digest())
    if encode:
        data = encode(data)
    return data

### 解密 ###
def tdecode(data, key, decode=base64.b64decode, salt_length=32):
    """RC4 decryption of encoded data"""
    if decode:
        data = decode(data)
    salt = data[:salt_length]
    return crypt(data[salt_length:], sha1(key + salt).digest())

#### ansible 执行脚本 ####
# def ansibleDoAction(ipaddress, user, password, cmds):
#     logging.info("Enter ansibleDoAction with successed .")
#     ret_list = []
#     ret_data = ''
#     for each_cmd in cmds:
#         # print "===========  ansible 开始执行 " + str(each_cmd) + " =================="
#         runner = ansible.runner.Runner(
#             host_list = [str(ipaddress)],  # 这里如果明确指定主机需要传递一个列表, 或者指定动态inventory脚本
#             module_name = 'shell',  # 模块名
#             module_args = each_cmd,  # 模块参数
#             extra_vars = {"ansible_ssh_user": user, "ansible_ssh_pass": password},
#             forks = 10
#         )
#         datastructure = runner.run()
#         data = json.dumps(datastructure, indent=4)
#         print "data:", data
#         print "===========  ansible 执行 " + str(each_cmd) + " 结束 =================="
#         if datastructure['contacted'] == {}:
#             if datastructure['dark'].has_key(ipaddress) == True:
#                 ret_num = 1
#                 ret_str = datastructure['dark'][ipaddress]['msg']
#             else:
#                 ret_num = 1
#                 ret_str = 'unknown error, more info to print data : ' + data
#         else:
#             ret_num = str(datastructure['contacted'][ipaddress]['rc'])
#             ret_str = str(datastructure['contacted'][ipaddress]['stderr'])
#         ret_list.append(ret_num)
#         ret_list.append(ret_str)
#         try:
#             ret_data = datastructure['contacted'][ipaddress]['stdout']
#         except Exception,e:
#             ret_data = 'Exception data:' + str(e)
#     return ret_data


####  ansible run ###
# def ansibleDoAction6(*parameters_list):
#     print "Enter ansibleDoAction with successed ."
#     ret_dict = {}
#     ipaddress, user, password, cmds = parameters_list[0][0], parameters_list[0][1], parameters_list[0][
#         2], parameters_list[0][3]
#     for i in range(len(cmds)):
#         print '===========  ansible 开始执行 ip:[ ' + str(ipaddress) + ' ], user:[ ' + str(user) + ' ],CMD=[ ' + str(cmds[i]) + ' ], 请等待 ... ============'
#         runner = ansible.runner.Runner(
#             host_list=[ipaddress],
#             module_name='shell',
#             module_args=cmds[i],
#             extra_vars={"ansible_ssh_user": user, "ansible_ssh_pass": password},
#             forks=10
#         )
#         datastructure = runner.run()
#         data = json.dumps(datastructure, indent=4)
#         print "data:", data
#         print '===========  ansible 执行 ip:[ ' + str(ipaddress) + ' ], user:[ ' + str(user) + ' ],CMD=[ ' + str(cmds[i]) + ' ], 结束  ============'
#         if datastructure['contacted'] == {}:
#             if datastructure['dark'].has_key(ipaddress) == True:
#                 ret_num = 1
#                 ret_str = datastructure['dark'][ipaddress]['msg']
#             else:
#                 ret_num = 1
#                 ret_str = 'unknown error, more info to print data : ' + data
#         else:
#             ret_num = str(datastructure['contacted'][ipaddress]['rc'])
#             ret_str = str(datastructure['contacted'][ipaddress]['stderr'])
#
#         if not ret_dict.has_key(ipaddress):
#             ret_dict[ipaddress] = {}
#         if not ret_dict[ipaddress].has_key(user):
#             ret_dict[ipaddress][user] = {}
#         if not ret_dict[ipaddress][user].has_key(i):
#             ret_dict[ipaddress][user][i] = {}
#         ret_dict[ipaddress][user][i]['command'] = cmds[i]
#         ret_dict[ipaddress][user][i]['ret_code'] = ret_num
#         ret_dict[ipaddress][user][i]['ret_str'] = ret_str
#     return ret_dict
    # queue.put(ret_dict)



#### 获取密码 ####
# def getUserOrgPassword(ip, user):
#     for i in range(len(allconnect)):
#         config_ip, config_user, config_encrypt_passwd = allconnect[i][0], allconnect[i][1], allconnect[i][2]
#         if config_ip == str(ip) and config_user == str(user):
#             return tdecode(config_encrypt_passwd, key)
#         else:
#             continue
#     return ''


# 获取 当前时间的 unix 时间戳 ，如：1484812395
def getUnixTimestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))

# 获得年月日时分秒的字符串 如： 201701191553
def timestamp_datetime(value):
    format = '%Y%m%d%H%M'
    value = time.localtime(value)
    return time.strftime(format, value)

# 返回唯一的目录名称
def onlyDirName():
    ctime = int(time.time())
    return str(timestamp_datetime(ctime)) + '_' + str(ctime)

#
def unixToDateTime(timeStamp):
    # timeStamp = 1381419600
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)