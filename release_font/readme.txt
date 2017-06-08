一、进入网页taskbegin。生成taskid，并根据json app发布类型写入发布步骤表。之后按步骤表执行发布过程。


二、点击clikcommand按钮执行发布步骤
下载上传  更新task_step表 下载上传步骤 状态为开始执行，并记录起始时间。
1、下载及重新打包。
将远端目录code和config目录下的文件下载到timedir/downloads文件夹内；
将downloads文件夹中的配置文件和war包重新打包，拷贝至timdir/pkg内。
通过 views:clikcommand ->taskcontroller:clickcommand -> taskcontroller:downloadfiles -> ftpcontrollerclass:downloadpkgs

2、按ip创建目录，将timedir/pkg 下的war包拷贝至 timedir/ip/appname/pkg下，将黄胜脚本拷贝至timedir/ip/appname/scprit/bin下
根据ip和appname查表获取黄胜脚本所需配置，将发布配置信息写至timedir/ip/appname/script/conf/app_config.conf中
将timedir/ip/ 目录按ip和用户同步至 对应ip发布机/autodeplay/timedir下
views:clikcommand ->taskcontroller:clickcommand -> taskcontroller:runUploadFilesToClients -> sycnlocaltool.syncloacl
更新task_step表 下载上传步骤 状态为完成，并记录结束时间。如异常终止发布，将状态改为异常。


执行检查
3、检查taskstep发布步骤表，is_stop字段为0时，开始执行检查步骤，为1时停止检查。
更新task_step表 check步骤 状态为开始执行，并记录起始时间。
并发调用黄胜check脚本。
当所有发布机所有应用的check脚本都正常执行完成。更新task_step表 check步骤 状态为完成，并记录结束时间。
taskcontroller:clickcommand->sycnlocaltool:runStep->paramikotool:runRemoteScriptProcess

4、其与步骤循环步骤3.

5、执行应用启动步骤。
根据upgradeapp应用配置表startsequence启动顺序启动应用。
目前已做到满足各种对应用启动顺序的要求。
具体实现:sycnlocaltool:runStep

6、回滚，is_stop字段为1到此停止执行。