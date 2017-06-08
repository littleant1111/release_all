#!/bin/bash

LOG_FILE=/tmp/a.log

main()
{
    log_echo "all parameters : $*  `who` is excuted "
}


log_echo()
{
    echo "[ `date "+%Y-%m-%d %H:%M:%S"` ]" $* | tee -a ${LOG_FILE}
}

main $*
