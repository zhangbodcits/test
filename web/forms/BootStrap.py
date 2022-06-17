# -*- coding: utf-8 -*-            
# @Time : 2022/6/17 15:48
# @Author:mr.Zhang
# @FileName: BootStrap.py
# @Software: PyCharm
class BootStrapForm(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入{}".format(field.label)
