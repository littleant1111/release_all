# release_all
包括2部分，发布前端和后端，按理安装django 设计，前端及模型设计好后，自带管理后端，但是考虑多人开发的情况，所以后端就是单独的应用来管理；

前端应用开发设计到 python sftp / paramiko / 多线程 / 和远程同步执行shell脚本等功能

前端应用的前端技术布局部门采取magicbox 和bootstrap + 和自定义css布局、jquery+ ajax。

前端demo： http://release.zdyw.tech/

设计背景介绍：
简单的发布如tomcat 就是将 *.war 包拷贝到目标应用 webapps 下，重启tomcat 是否启动成功；
复杂的是
1、有些发布并不是tomcat 容器，比如使用的是weblogic 、glashfish等等容器；
2、发布目标应用部署的是集群方式，比如一个应用部署在20台机器上面，手工发布工作重复且效率低下，出错率大，发布慢；
3、如果一个项目或者系统包括多个应用，则发布机器会成倍增加；

为了能够解决上述问题，研发了此套发布系统，实现流程也需要详细说下：
1、配置文件怎么解决；<br/>
2、编译出来的war包存放在哪？
3、应用发布，应用和机器以及用户等等部署信息怎么配置？







































