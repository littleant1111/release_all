#!/bin/bash

#######     combine package and config   #####

if [ `echo "$0" |grep -c "/"` -gt 0 ];then
    cd ${0%/*}
fi

PROGRAM_DIR=`pwd`
cd ..
BASE_DIR=`pwd`
PROGRAM_NAME=`basename $0`
DATE=`date +'%Y%m%d_%H%M'`
TS=`date +%s`

TEMP_DIR=${BASE_DIR}/temp
LOG_DIR=${BASE_DIR}/log
CONFIG_DIR=${BASE_DIR}/conf
BIN_DIR=${BASE_DIR}/bin
LOG_FILE=${LOG_DIR}/${PROGRAM_NAME}.log

. ${BASE_DIR}/bin/pub.lib



main()
{
    if [ $# -ne 4 ];then
        showHelp
        return 1
    fi
    
    g_only_dir_name="$1"
    g_pkg_dir="$2"
    g_cfg_dir="$3"
    g_tartet_dir="$4"
    
    ONLY_DIR=${TEMP_DIR}/${g_only_dir_name}
    typeset eachline=""
    
    checkBaseEnv || return 1
    
    tmpFile=${TEMP_DIR}/tmp.tmp
    find ${g_pkg_dir} -name "*.war" > ${tmpFile}
    if [ ! -s "${tmpFile}" ];then
        log_echo "ERROR" "main" "Not find one war package, please check dir:[  ${g_pkg_dir}  ]"
        return 1
    fi
    typeset linenum=`cat ${tmpFile} | wc -l`
    if [ "${linenum}" -gt 1 ];then
        log_echo "ERROR" "main" "Find more than one package."
        return 1
    fi
    typeset pkgname=`cat ${tmpFile} | head -1`
    pkgname=`basename ${pkgname}`
    typeset prefixPkgName=`echo "${pkgname%.*}"`
    pkg_file=${g_pkg_dir}/${pkgname}
    
    # unzip war test
    log_echo "INFO" "$func" "Unzip pkg:[ ${pkg_file} ] to dir:[ ${ONLY_DIR}/${prefixPkgName} ] ,please wait . "
    rm -rf ${ONLY_DIR}/${prefixPkgName} && unzipWar ${pkg_file} ${ONLY_DIR}/${prefixPkgName} || return 1
    log_echo "info" "$func" "Unzip pkg:[ ${pkg_file} ] to dir:[ ${ONLY_DIR}/${prefixPkgName} ]  with successed. "
    
    ##### �������ļ�����ԭ������������ļ�   ###########
    cp -rf  ${g_cfg_dir}/*   ${ONLY_DIR}/${prefixPkgName}
    if [ $? -ne 0 ];then
        log_echo "ERROR" "$func" "Cover config file from:[ ${g_cfg_dir} ] to dir : [ ${ONLY_DIR}/${prefixPkgName} ] with Failed.CMD=[  cp -rf  ${g_cfg_dir}/*   ${ONLY_DIR}/${prefixPkgName}  ] , please check ."
        return 1
    fi
    log_echo "INFO" "$func" "Cover config file from:[ ${g_cfg_dir} ] to dir : [ ${ONLY_DIR}/${prefixPkgName} ] with successed "
    
    ### zip a new package ####
    log_echo "INFO" "$func" "Zip file from:[ ${ONLY_DIR}/${prefixPkgName} ] to file:[ ${ONLY_DIR}/${prefixPkgName}/${pkgname} ] with successed and copy file to dir:[ ${g_tartet_dir} ], please wait ... "
    cd ${ONLY_DIR}/${prefixPkgName} && zip -r ${pkgname} *  >/dev/null 2>&1 && rm -f ${g_tartet_dir}/${pkgname} && cp -f ${ONLY_DIR}/${prefixPkgName}/${pkgname}  ${g_tartet_dir} 
    if [ $? -ne 0 ];then
        log_echo "ERROR" "$func" "Zip file from:[ ${ONLY_DIR}/${prefixPkgName} ] to file:[ ${ONLY_DIR}/${prefixPkgName}/${pkgname} ] with successed and copy file to dir:[ ${g_tartet_dir} ], with failed . "
    fi
    log_echo "INFO" "$func" "Zip file from:[ ${ONLY_DIR}/${prefixPkgName} ] to file:[ ${ONLY_DIR}/${prefixPkgName}/${pkgname} ] with successed and copy file to dir:[ ${g_tartet_dir} ], with successed . "
    log_echo "INFO" "$func" "Exit main with successed."
    return 0    
}

####    ###

#### base env check and config  #####
checkBaseEnv()
{
    typeset func=checkBaseEnv
    typeset flag=0 
    typeset eachDir=""
    typeset eachScript=""
    typeset eachCheckFile=""
    log_echo "info" "$func" "Enter $func with successed."
    for eachDir in ${TEMP_DIR}  ${LOG_DIR}  ${CONFIG_DIR}  ${BIN_DIR} ${ONLY_DIR};do
        mkdir -p ${eachDir}
        if [ $? -ne 0 ];then
            log_echo "error" "Command is error,CMD = [     mkdir -p ${eachDir}    ]"
            flag=1    
        fi
    done
    if [ ! -f "${LOG_FILE}" ];then
        touch ${LOG_FILE} && chmod 666 ${LOG_FILE}
        if [ $? -ne 0 ];then
            log_echo "error" "Command is error,CMD = [     touch ${LOG_FILE} && chmod 666 ${LOG_FILE}     ]"
            flag=1    
        fi
    fi
    checkDirsExists "${g_tartet_dir}" || return 1
    log_echo "info" "$func" "Exit $func with successed."
    return 0
}    

## show how to use this script   ##
showHelp()
{

cat << EOF
  
This script is used to auto combine package and config files

USAGE: ${PROGRAM_NAME} [-help|--help] 

OPTIONS:
   
  para1: [ help | {only_dir_name} ]
        --help| -help :                  Display this help
         only_dir_name:                  only dir name                                
 
  para2: pkg_dir                         config files base dir
  
  para3: config_base_dir                 config files base dir
  
  para4: target_dir                      new package dir

EXAMPLE: 

EOF

    return 0
}

main $*    