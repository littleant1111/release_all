#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.contrib import admin

# Register your models here.
from release.models import env,env_child,project
admin.site.register(env)
admin.site.register(env_child)
admin.site.register(project)