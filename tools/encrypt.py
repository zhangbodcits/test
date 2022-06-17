# -*- coding: utf-8 -*-            
# @Time : 2022/6/17 11:55
# @Author:mr.Zhang
# @FileName: encrypt.py
# @Software: PyCharm
from django.conf import settings


def md5(string):
    import hashlib

    hash_object = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    hash_object.update(string.encode(encoding='utf-8'))
    return hash_object.hexdigest()
