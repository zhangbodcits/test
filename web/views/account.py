# -*- coding: utf-8 -*-            
# @Time : 2022/6/15 16:06
# @Author:mr.Zhang
# @FileName: account.py
# @Software: PyCharm
from django.shortcuts import render, HttpResponse
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm
from django.http import JsonResponse
from App import models


def register(request):
    '''注册'''
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库
        form.save()
        return JsonResponse({"status": True, "data": "/login_sms/"})

    return JsonResponse({"status": False, "error": form.errors})


def send_sms(request):
    '''发送短信'''
    # print(request.GET)
    form = SendSmsForm(request, data=request.GET)
    # 校验手机号不能为空，格式是否正确
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {"form": form})
    form = LoginSMSForm(data=request.POST)
    if form.is_valid():
        # 用户名输入正确
        mobile_phone = form.cleaned_data["mobile_phone"]
        # 把用户写入到session中
        user_object = models.sys_user.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id'] = user_object.id
        request.session['user_name'] = user_object.user_name

        return JsonResponse({"status": True, 'data': "/index/"})
    return JsonResponse({"status": False, 'error': form.errors})
