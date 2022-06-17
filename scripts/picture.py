# -*- coding: utf-8 -*-            
# @Time : 2022/6/17 17:07
# @Author:mr.Zhang
# @FileName: picture.py
# @Software: PyCharm
from PIL import Image

img = Image.new(mode="RGB", size=(120, 30), color=(255, 255, 255))
with open('code.png', 'wb') as f:
    img.save(f, format='png')
