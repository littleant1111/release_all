#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse


class LoginControllerClass(object):

    # 检测是否有session 构造函数
    def __init__(self, request):
        self.request = request

    def login(self):
        # def login(request):
        username, password = self.request.POST.get('username', ''), self.request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(self.request, user)
            self.request.session['user'] = username
            return redirect('/release/index/')
        else:
            return render(self.request, 'login.html')

    # 检测是否有session
    def is_logined(self):
        if self.request.session.get('user') is None:
            return False
        else:
            return True

    # 登录到首页
    def index(self):
        if self.is_logined() == True:
            return render(self.request, 'index.html')
        else:
            return self.login()
    # 退出
    def logout(self):
        auth.logout(self.request)
        return self.login()

    # 密码更改
    def password_change(self):
        if self.request.method == 'POST':
            form = PasswordChangeForm(user=self.request.user, data=self.request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(self.request, form.user)
                return HttpResponseRedirect(reverse('release:password_change_done'))
        else:
            form = PasswordChangeForm(user=self.request.user)
        return render(self.request, 'password_change.html', {'form':form})



















