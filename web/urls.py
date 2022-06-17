# -*- coding: utf-8 -*-            
# @Time : 2022/6/15 16:58
# @Author:mr.Zhang
# @FileName: urls.py
# @Software: PyCharm
from django.conf.urls import url, include
from django.contrib import admin
from web.views import account

urlpatterns = [
    url(r'^register/$', account.register, name="register"),
    url(r'^send_sms/$', account.send_sms, name="send_sms"),
    url(r'^login_sms/$', account.login_sms, name="login_sms"),
    url(r'^index/$', account.register, name="index"),
]
