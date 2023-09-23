import json
import os
import urllib
import uuid
from urllib.parse import urlparse
from urllib.request import urlretrieve

import requests


def sendImg(img_path, img_name, img_type='image/jpeg'):
    """
    :param img_path:图片的路径
    :param img_name:图片的名称
    :param img_type:图片的类型,这里写的是image/jpeg，也可以是png/jpg
    """
    url = 'http://tiyupc.com/api.php/web/index/scrayd_image_store'  # 自己想要请求的接口地址

    with open(img_path + img_name, "rb")as f_abs:  # 以2进制方式打开图片
        body = {
            # 有些上传图片时可能会有其他字段,比如图片的时间什么的，这个根据自己的需要
            'img': (img_name, f_abs, img_type),
            # 图片的名称、图片的绝对路径、图片的类型（就是后缀）
            "time": (None, "2019-01-01 10:00:00")

        }
        # 上传图片的时候，不使用data和json，用files
        response = requests.post(url=url, files=body)
        result = eval(response.text)
        print(result['data'])
        if result['code'] == 200:
            return 'http://tiyupc.com' + result['data']['url']
        else:
            return False


response = sendImg('E:/Company/WorkPlace/system/images/2020424/', '0a04979190f54c1ea7dc68f3fb8351c2.png')
print(response)
# def get_filename(url_str):
#     url = urlparse(url_str)
#     print(url)
#     i = len(url.path) - 1
#     while i > 0:
#         if url.path[i] == '/':
#             break
#         i = i - 1
#     filename = url.path[i + 1:len(url.path)]
#     if not filename.strip():
#         return False
#     return filename
