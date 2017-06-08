#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paramiko
import sys
import os


def putwar(hostname, port, username, password, remote_dir, version, file):
    try:
        t = paramiko.Transport((str(hostname), int(port)))
        t.connect(username=str(username), password=str(password))
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.chdir(remote_dir + os.sep + 'code')
        try:
            sftp.mkdir(version)
        except Exception, e:
            print 'file exists'
        sftp.chdir(remote_dir + os.sep + 'config')
        try:
            sftp.mkdir(version)
        except Exception, e:
            print 'file exists'
        remotefile = file.split('/')[-1:][0]
        print file, remote_dir + os.sep + version + os.sep + remotefile
        sftp.put(file, remote_dir + os.sep + 'code' + os.sep + version + os.sep + remotefile)

        t.close()
    except Exception, e:
        print 'aaaa', e


if __name__ == '__main__':
    version = sys.argv[1]
    localpath = sys.argv[2]
    project = sys.argv[3]
    listfile = []
    for file in os.listdir(localpath + os.sep + 'target'):
        if '.war' in file:
            listfile.append(localpath + os.sep + 'target' + os.sep + file)

            print file
    print listfile
    for war in listfile:
        print war
        putwar('10.80.7.84', '22', 'uatuser', '!QAZxsw2', '/'+project, version, war)