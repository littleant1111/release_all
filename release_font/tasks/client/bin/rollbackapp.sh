#!/bin/bash
# Filename: rollbackapp.sh
# Revision: 1.0
# Date: 2017/02/15
# Email: sheng.huang@bqjr.cn
# Usage: bash rollbackapp.sh
# 功能：根据上次更新留下的备份包进行回滚
# 详细如下：
#     判断容器类型，通过临时配置文件中的变量获取到上次更新留下的备份包进行回滚操作，并启动应用。
#     脚本运行会检测是否已经过checkapp步骤，否则不会继续执行。
# 返回值： 正常 0；  不正常 1

# 脚本获取绝对路径，使不受运行位置影响
if [ `echo "$0" |grep -c "/"` -gt 0 ];then
    cd ${0%/*}
fi

PROGRAM_DIR=`pwd`
cd ..
BASE_DIR=`pwd`
PROGRAM_NAME=`basename $0`

# 加载运行所需函数库
. ${BASE_DIR}/bin/pub.lib

# 加载环境变量
. /etc/profile

# 定义目录名变量
TEMP_DIR=${BASE_DIR}/temp
LOG_DIR=${BASE_DIR}/log
CONFIG_DIR=${BASE_DIR}/conf
BIN_DIR=${BASE_DIR}/bin

# 定义文件名变量
LOG_FILE=${LOG_DIR}/${PROGRAM_NAME}.log
APP_CONF=${CONFIG_DIR}/app_config.conf
TEMPORARY_STORAGE_CONF=${CONFIG_DIR}/temporary_storage_app.conf

# 加载文件中的变量
. ${APP_CONF}
. ${TEMPORARY_STORAGE_CONF}

# 脚本运行程序入口
main(){
    typeset func=main
    if [ $# -ne 0 ];then
        log_echo "[error]" "${func}" "Parameter error , ${PROGRAM_NAME} no use anyone parameter "
        return 1
    fi
    log_echo "[info] Enter ${func} with successed ." 

    # 检测当前执行用户非root
    detectionRootUser || return 1

    # 回滚前检测配置文件是否存在
    if [ ! -f ${TEMPORARY_STORAGE_CONF} ];then
        log_echo "[error]" "Monitoring to the configuration file does not exist, please check whether there is a backup operation, automatic withdrawal"
        return 1
    fi

    # 判断备份变量是否存在
    if [ -z ${tomcatBackupName} ];then
        log_echo "[error]" "Check to backup the variable name does not exist, automatically exit"
        return 1
    fi

    # 判断备份文件包是否存在
    checkFilesExists ${tomcatBackupName} || return 1
    
    # 回滚前检测应用是否运行，若运行先停止
    getUserJavaProcessesId ${user[1]} ${appdir[1]} || return 1
    appjaveids="${RETURN[0]}"
    if [ -z "${appjaveids}" ];then
        log_echo "[info]" "Not found java processes ,the application is not running"
    else   
        for appjaveid in `echo "${appjaveids}"`;do
            log_echo "[info]" "Stop the application before rollback"
            log_echo "[info]" "To kill the process number ${appjaveid}"
            # 记录即将杀死进程详细信息
            typeset processesInformaiton=`ps -ef | grep ${appjaveid} | grep java | grep ${user[1]} | grep ${appdir[1]}` >> /dev/null 2>&1
            log_echo "[info]" "Process details are as follows"
            log_echo "${processesInformaiton}"
            kill -9 ${appjaveid}
            if [ $? -ne 0 ];then
                log_echo "[error]" "Exec command error , CMD = [  kill -9 ${appjaveid}  ]"
                return 1
            fi
        done
        log_echo "[info]" "stop tomcat successed. : tomcat dir: [ ${appdir[1]} ] with user : [ ${user[1]} ]  pid : [ ${appjaveid} ]"
    fi
    
    # 根据容器类型进行操作
    if [ ${apptype[1]} == "tomcat" ];then
        # 通过存储路径获取包名
        typeset appwarname=`stringToIntercept ${pkgfile}` || return 1
        typeset localTime=`date "+%Y%m%d%H%M%S"`

        # 定义回滚容器内文件存放目录名
        typeset rollbackBackupdir="${TEMP_DIR}/${projectname}_${version}/${projectname}_${version}_${localTime}_rollback"
        # 创建存储回滚缓存和代码目录
        log_echo "[info]" "Create a unique rollback directory name [ ${rollbackBackupdir} ]"
        mkdir -p "${rollbackBackupdir}/webapps"
        judgeCommandFailureExit
        mkdir "${rollbackBackupdir}/work" && mkdir "${rollbackBackupdir}/temp"
        judgeCommandFailureExit
        
        # 移动缓存 并拷贝更新包到tomcat中
        log_echo "[info]" "Begin to rollback ,please wait..."
        log_echo "[info]" "Execute the command : [ mv ${appdir[1]}/work/* ${rollbackBackupdir}/work ] [ mv ${appdir[1]}/temp/* ${rollbackBackupdir}/temp ] [ mv ${appdir[1]}/webapps/* ${rollbackBackupdir}/webapps ] "
        mv ${appdir[1]}/work/* "${rollbackBackupdir}/work" 
        judgeCommandFailureWarning
        mv ${appdir[1]}/temp/* "${rollbackBackupdir}/temp" 
        judgeCommandFailureWarning
        mv ${appdir[1]}/webapps/* "${rollbackBackupdir}/webapps"
        judgeCommandFailureExit
        
        # 解压备份包到容器内
        log_echo "[info]" "Unpack the backup package to the container"
        tar -xf ${tomcatBackupName} -C ${appdir[1]}/webapps/ || return 1
        judgeCommandFailureExit || return 1
        
        # 启动应用程序
        log_echo "[info]" "To start the tomcat application"
        startTomcatApply ${appwarname} ${user[1]} ${appdir[1]} ${startuptime[1]} || return 1
        judgeCommandFailureExit || return 1
        
    elif [ ${apptype[1]} == "weblogic" ];then
        log_echo "[info]" "Weblogic container, temporarily does not support automatic exit"  
    else
        log_echo "[info]" "Container type error or temporary does not support, automatic withdrawal"   
    fi
    
    log_echo "[info]" "Exit func ${func} with successed."
    log_echo "[info]" "回滚应用成功 || Roll back the application successfully "
    return 0 
}

main $* || exit 1
