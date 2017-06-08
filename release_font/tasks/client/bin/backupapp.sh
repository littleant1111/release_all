#!/bin/bash
# Filename: backupapp.sh
# Revision: 1.1
# Date: 2017/02/15
# Email: sheng.huang@bqjr.cn
# Usage: bash backupapp.sh
# 功能：备份应用程序中的代码 
# 详细如下：
#     通过判断容器类型，将容器内所有代码备份到指定目录
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

# 定义目录名变量
TEMP_DIR=${BASE_DIR}/temp
LOG_DIR=${BASE_DIR}/log
CONFIG_DIR=${BASE_DIR}/conf
BIN_DIR=${BASE_DIR}/bin

# 定义文件名变量
LOG_FILE=${LOG_DIR}/${PROGRAM_NAME}.log
APP_CONF=${CONFIG_DIR}/app_config.conf
OSCHECK_CONF=${CONFIG_DIR}/oscheck_config.conf
TEMPORARY_STORAGE_CONF=${CONFIG_DIR}/temporary_storage_app.conf

# 加载文件中的变量
. ${APP_CONF}
. ${OSCHECK_CONF}

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
    
    # 检查是否已经过checkapp步骤
    log_echo "[info]" "Check whether have been checkapp steps"
    if [ -f "${TEMPORARY_STORAGE_CONF}" ];then
        . ${TEMPORARY_STORAGE_CONF}
        judgmentVariableExist "safeLock" || return 1
        if [ "${safeLock}" != "checkapp" ];then
            log_echo "[error]" "In the file [ ${TEMPORARY_STORAGE_CONF} ] not found in the safety lock or safety lock step is not equal to [checkapp], please check first step checkapp.sh"
            return 1
        fi
    else
        log_echo "[error]" "Not found the safety lock file ${TEMPORARY_STORAGE_CONF}, automatically exit"
        return 1
    fi
    
    # 开始备份
    log_echo "[info]" "Start backup application"
    typeset localTime=`date "+%Y%m%d%H%M%S"`
    backupApply ${apptype[1]} ${backupdir[1]} ${projectname} ${version} ${localTime} ${appdir[1]} || return 1

    typeset tomcatBackupName=${backupdir[1]}/${projectname}_${version}/${projectname}_${version}_${localTime}.tar.gz

    checkFilesExists ${tomcatBackupName} || return 1
    if [ $? -eq 0 ];then
        # 将本次备份文件记录到临时文件中，供回滚脚本使用
        log_echo "[info]" "Create a of the backup file path to a temporary file"
        if [ -f "${TEMPORARY_STORAGE_CONF}" ];then
            grep "tomcatBackupName" ${TEMPORARY_STORAGE_CONF} >> /dev/null 2>&1
            if [ $? -eq 0 ];then
                sed -i "s#^tomcatBackupName.*#tomcatBackupName=${tomcatBackupName}#" ${TEMPORARY_STORAGE_CONF}
            else
                echo "tomcatBackupName=${tomcatBackupName}" | tee -a ${TEMPORARY_STORAGE_CONF} >> /dev/null 2>&1
            fi
        else
            echo "tomcatBackupName=${tomcatBackupName}" | tee -a ${TEMPORARY_STORAGE_CONF} >> /dev/null 2>&1
        fi
        log_echo "[info]" "Backup file [ ${tomcatBackupName} ] detection, backup successfully"
    else
        log_echo "[error]" "Backup application directory failed, please check the file whether there is ${tomcatBackupName}"
        return 1
    fi

    log_echo "[info]" "Exit func ${func} with successed."
    log_echo "[info]" " 备份应用成功 || Backup application successfully "
    return 0 
}

main $* || exit 1

