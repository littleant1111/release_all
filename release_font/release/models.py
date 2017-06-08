#!/usr/bin/python
# -*- coding: UTF-8 -*-
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models

class env(models.Model):
    name = models.CharField(u'发布环境',max_length=20)
    remark = models.CharField(u'环境描述',max_length=50,blank=True)


    class Meta:
        verbose_name = u"环境"
        verbose_name_plural = u"环境"

class env_child(models.Model):
    envchild_name = models.CharField(u'发布子环境',max_length=24)
    env_id = models.ForeignKey(env)


    class Meta:
        verbose_name = u"子环境"
        verbose_name_plural = u"子环境"

class project(models.Model):
    name = models.CharField(u'项目名',max_length=20)
    remark = models.CharField(u'项目描述',max_length=50,blank=True)
    env_child = models.ManyToManyField('env_child')


    class Meta:
        verbose_name = u"项目"
        verbose_name_plural = u"项目"

class config(models.Model):
    item = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    remark = models.CharField(max_length=255)
    project_env_id = models.IntegerField()

