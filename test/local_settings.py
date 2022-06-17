# -*- coding: utf-8 -*-            
# @Time : 2022/6/14 16:13
# @Author:mr.Zhang
# @FileName: local_settings.py
# @Software: PyCharm
LANGUAGE_CODE = 'zh-hans'
# 腾讯云短信应用的app_id
TENCENT_SMS_APP_ID = 1400693463
# 腾讯云短信应用的app_key
TENCENT_SMS_APP_KEY = "cbdbce6baf79e82e5449a5b0a99e3b6d"
# 腾讯云短信应用的签名内容
TENCENT_SMS_SIGN = "博古冠今"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.110.104:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "foobared" # redis密码
        }
    }
}
