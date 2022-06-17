# -*- coding: utf-8 -*-            
# @Time : 2022/6/15 17:59
# @Author:mr.Zhang
# @FileName: account.py
# @Software: PyCharm
from django.shortcuts import render, HttpResponse

from django import forms
from App import models
from django.core.validators import RegexValidator, ValidationError
from django.conf import settings
import random
from tools.tencent.sms import send_sms_single
from tools import encrypt
from django_redis import get_redis_connection
from web.forms.BootStrap import BootStrapForm


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机号格式错误！")])
    password = forms.CharField(
        label="密码",
        min_length=8,
        max_length=64,
        error_messages={
            "min_length": "密码长度不能小于8位字符",
            "max_length": "密码长度不能大于64位字符",
        },
        widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label="重复密码",
        min_length=8,
        max_length=64,
        error_messages={
            "min_length": "密码长度不能小于8位字符",
            "max_length": "密码长度不能大于64位字符",
        },
        widget=forms.PasswordInput())
    code = forms.CharField(label="验证码", widget=forms.TextInput())

    class Meta:
        model = models.sys_user
        fields = "__all__"
        # fields = ['username', 'email', 'mobile_phone', 'code', 'password', 'confirm_password']

    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = models.sys_user.objects.filter(username=username).exists()
        if exists:
            # raise ValidationError("用户名已存在")
            self.add_error('username', "用户名已存在")
            return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        return encrypt.md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = encrypt.md5(self.cleaned_data["confirm_password"])
        if password != confirm_password:
            raise ValidationError("两次输入密码不一致")
        return confirm_password

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data["mobile_phone"]
        exists = models.sys_user.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data["code"]
        mobile_phone = self.cleaned_data["mobile_phone"]
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码失效或未发送")
        str_redis_code = redis_code.decode('utf-8')
        if code.strip() != str_redis_code:
            raise ValidationError("验证码不正确，请重新输入")
        return code


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label="手机号",
                                   validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机号格式错误！")])

    # 把视图中的request传进来
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        """手机号检验的钩子"""
        mobile_phone = self.cleaned_data['mobile_phone']
        # 判断短信模板是否存在
        tpl = self.request.GET.get("tpl")
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError("短信模板不存在")
        exists = models.sys_user.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == "login":
            if not exists:
                raise ValidationError("手机号不存在")
        else:
            # 判断手机号是否已存在

            if exists:
                raise ValidationError("手机号已存在")
        code = random.randrange(1000, 9999)
        print(code, 11111111111111)
        # 发送短信
        sms = send_sms_single(mobile_phone, template_id, [code])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败，{}".format(sms['errmsg']))
        # 验证码写入redis
        conn = get_redis_connection("default")
        conn.set(mobile_phone, code, ex=60)

        return mobile_phone


class LoginSMSForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机号格式错误！")])
    code = forms.CharField(label="验证码", widget=forms.TextInput())

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data["mobile_phone"]
        user_object = models.sys_user.objects.filter(mobile_phone=mobile_phone).first()
        exits = models.sys_user.objects.filter(mobile_phone=mobile_phone).exists()
        if not exits:
            raise ValidationError("手机号不存在")
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data["code"]
        mobile_phone = self.cleaned_data.get("mobile_phone")
        # 手机号不存在
        if not mobile_phone:
            return code
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码失效或未发送")
        str_redis_code = redis_code.decode('utf-8')
        if code.strip() != str_redis_code:
            raise ValidationError("验证码不正确，请重新输入")
        return code
