#!/bin/bash
# Filename: checkapp.sh
# Revision: 1.1
# Date: 2017/02/15
# Email: sheng.huang@bqjr.cn
# Usage: bash checkapp.sh
# 功能：检查更新应用容器的运行环境和自身脚本所需的配置文件
# 详细如下：
#     检查自身需要的目录conf、log、temp和配置文件app_conf.conf、os_conf.conf是否存在
#     检查tomcat基础运行环境如基础命令(curl,zip,expect等)是否存在，硬件资源内存，CPU，硬盘是否充足等(第一版暂不开启，已注释)
#     检查配置文件内容如，应用目录，备份目录，更新包、支持的容器类型和更新类型，IP是否为本机等
#     原则上本文件需要考虑到更新过程中所有可能遇到的情况，检查不通过不允许进行其他脚本运行
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

# 定义目录变量
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
    log_echo "[info] Enter ${func} with successed ." 
    
    if [ $# -ne 0 ];then
        log_echo "[error]" "${func}" "Parameter error , ${PROGRAM_NAME} no use anyone parameter "
        return 1
    fi
    
    # 检测当前执行用户非root
    detectionRootUser || return 1
    
    # 检查脚本文件个数
    if [ `ls "${BIN_DIR}"/* | wc -l` -ne 7 ];then
        log_echo "[error]" "Check the script file number error, details are as follows."
        ls "${BIN_DIR}"/*
        return 1
    fi
    
    # 检查基础文件夹是否存在  
    log_echo "[info]" "Check the base folder exists"
    for eachDir in ${TEMP_DIR} ${LOG_DIR} ${CONFIG_DIR};do
        checkDirExists ${eachDir} || return 1
    done
    
    # 检查配置文件是否存在
    log_echo "[info]" "Check the configuration file exists"
    checkFilesExists ${APP_CONF} ${OSCHECK_CONF} || return 1
    
    # 检查变量名是否存在
    # 此处需要王梓增加一个新的变量 如check_cmd=(unzip cp touch rm) 增加后可用循环检查加判断，自已做个数判断无意义 
    log_echo "[info]" "Check whether the variable name"
    # for each_variable in ${check_variables[@]};do
        # judgmentVariableExist ${each_variable} || return 1
    # done
    judgmentVariableExist ${pkgfile} || return 1
    judgmentVariableExist ${version} || return 1
    judgmentVariableExist ${appdir[1]} || return 1
    judgmentVariableExist ${appnumber} || return 1
    judgmentVariableExist ${projectname} || return 1
    judgmentVariableExist ${appdir[1]} || return 1
    judgmentVariableExist ${ip} || return 1    
    judgmentVariableExist ${user[1]} || return 1    
    judgmentVariableExist ${upgradetype[1]} || return 1
    judgmentVariableExist ${apptype[1]} || return 1  
    judgmentVariableExist ${backupdir[1]} || return 1   
    judgmentVariableExist ${startuptime[1]} || return 1 
    
    # 检查应用目录是否存在
    log_echo "[info]" "Check the ${appdir[1]}"
    checkDirExists ${appdir[1]} || return 1

    # 检查应用目录下启动文件执行权限
    log_echo "[info]" "Check the file ${appdir[1]}/bin/catalina.sh execute permissions"
    checkFilesExecutePermissions ${appdir[1]}/bin/catalina.sh || return 1
        
    # 检查备份目录是否存在
    log_echo "[info]" "Check the ${backupdir[1]}"
    if [ ! -d "${backupdir[1]}" ];then
        log_echo "[warn]" "Folder does not exist, ${backupdir[1]} detected automatically created"
        mkdir -p ${backupdir[1]}
        judgeCommandFailureExit || return 1
    fi
    
    # 检查备份目录是否有写入权限
    log_echo "[info]" "Check the backup directory ${backupdir[1]} for write access"
    echo "Check the backup directory ${backupdir[1]} for write access,Test to use, can be deleted." > ${backupdir[1]}/checkapp_tmp_file.txt 
    judgeCommandFailureExit || return 1

    # 检查配置文件中ip是否为本机
    # log_echo "[info]" "Check the local ${ip}"
    # getLocalIp 
    # if [ "${RETURN[0]}" != "${ip}" ];then
        # log_echo "[error]" "Check whether the local ${ip} error"
        # return 1
    # fi 
      
    # 检查应用类型是否为tomcat或weblogic  同下 暂不需要
    # log_echo "[info]" "Check the application type is tomcat or weblogic"
    # if [ "${apptype[1]}" != "tomcat" -a "${apptype[1]}" != "weblogic" ];then
        # log_echo "[error]" "Check the application type error, temporarily does not support"
        # return 1
    # fi
    
    # 检查app应用类型和更新类型 目前只支持 tomcat 全量更新
    log_echo "[info]" "Start check application type"
    checkApply ${apptype[1]} ${upgradetype[1]} || return 1
    
    # 检查url是否可以访问
    #log_echo "[info]" "Check the ${url[1]}"
    #canOpenUrl ${url[1]}
    #judgeCommandFailureExit
    
    # 检查更新包是否能正常解压
    log_echo "[info]" "Check the ${pkgfile}"
    mkdir -p ${TEMP_DIR}/tempUnzip
    judgeCommandFailureExit || return 1
    tempUnzipDir=${TEMP_DIR}/tempUnzip
    checkUnzipWar ${pkgfile} ${tempUnzipDir} || return 1
            
    # typeset func=checkOsEnv
    # log_echo "[info]" "Enter ${func} with successed"
    # # 检查基础命令是否存在
    # for each_cmd in ${check_cmd[@]};do
        # checkCommadExist ${each_cmd} || return 1
    # done
    # # 检查os硬件部分信息
    # CheckOsHardwareInformation "${hardDisk}" || return 1
    # tail -${CheckOsHardwareInformationLine} ${LOG_FILE}
    # CheckOsHardwareInformation "${freeMemory}" || return 1
    # tail -${CheckOsHardwareInformationLine} ${LOG_FILE}
    # # CheckOsHardwareInformation "${cpuProcessor}"
    # # tail -${CheckOsHardwareInformationLine} ${LOG_FILE}
    # # `${cpuProcessor}` >> ${LOG_FILE}
    # log_echo "[info]" "当前系统cpu核数" "`cat /proc/cpuinfo | grep 'processor' | wc -l`"
    # # 检查基础应用部分
    # CheckOsHardwareInformation "${appdir[1]}/bin/version.sh | tail -8" || return 1
    # typeset CheckOsHardwareInformationLine_tomcat=`expr ${CheckOsHardwareInformationLine} - 5`
    # tail -${CheckOsHardwareInformationLine_tomcat} ${LOG_FILE}
    # CheckOsHardwareInformation "${pythonVersion}" || return 1
    # typeset CheckOsHardwareInformationLines_python=`expr ${CheckOsHardwareInformationLine} - 1`
    # tail -${CheckOsHardwareInformationLines_python} ${LOG_FILE}
    # log_echo "[info]" "Exit ${func} with successed ."

    # 增加安全锁机制，供后面步骤检查确认已执行检查操作
    log_echo "[info]" "Create a security lock variable to a temporary file"
    if [ -f "${TEMPORARY_STORAGE_CONF}" ];then
        grep "safeLock" ${TEMPORARY_STORAGE_CONF} >> /dev/null 2>&1
        if [ $? -eq 0 ];then
            sed -i "s#^safeLock.*#safeLock=checkapp#" ${TEMPORARY_STORAGE_CONF}
        else
            echo "safeLock=checkapp" | tee -a ${TEMPORARY_STORAGE_CONF} >> /dev/null 2>&1
        fi
    else
        echo "safeLock=checkapp" | tee -a ${TEMPORARY_STORAGE_CONF} >> /dev/null 2>&1
    fi
    log_echo "[info]" "Create a security lock variable to the temporary file successfully"
            
    log_echo "[info] Exit main() with successed ."
    log_echo "[info]" "检查各项基础内容成功通过 || Check all the basics by success"
    return 0
}

main $* || exit 1

# 待改进问题记录
# 需要判断备份目录容量 再检测容量空间时
# 去掉核对ip的步骤
# 新增检查运行脚本个数

