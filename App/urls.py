# -*- coding: utf-8 -*-            
# @Time : 2022/6/15 16:54
# @Author:mr.Zhang
# @FileName: urls.py
# @Software: PyCharm
from django.conf.urls import url, include
from django.contrib import admin
from App import views

urlpatterns = [
    url(r'^register/', views.register),
    url(r'^index/', views.index),
]