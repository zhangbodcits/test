from django.shortcuts import render, HttpResponse
from tools.tencent.sms import send_sms_single
import random
from django.conf import settings


# Create your views here.
def send_sms(request):
    tpl = request.GET.get("tpl")
    print(tpl, 111111111111)
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse("模板不存在")
    code = random.randrange(1000, 9999)
    res = send_sms_single("15035461679", template_id, [code])
    print(res)
    if res["result"] == 0:
        return HttpResponse("短信发送成功")
    else:
        return HttpResponse(res['errmsg'])


from django import forms
from App import models
from django.core.validators import RegexValidator


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机号格式错误！")])
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="重复密码", widget=forms.PasswordInput())
    code = forms.CharField(label="验证码")

    class Meta:
        model = models.sys_user
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入{}".format(field.label)


def register(request):
    form = RegisterModelForm()
    return render(request, "App/register.html", {"form": form})

from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
def index(request):
    # 去连接池中获取一个连接
    conn = get_redis_connection("default")
    conn.set('nickname', "张博", ex=10)
    value = conn.get('nickname')
    print(value)
    return HttpResponse("OK")
