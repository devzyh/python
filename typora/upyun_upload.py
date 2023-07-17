"""
作者：devzyh
时间：2023-07-14
描述：Typora图片上传又拍云客户端
"""
import io
import os.path
import sys
import uuid
from urllib.parse import urlparse

import requests

img_list = sys.argv[1:]
domain = "https://img.devzyh.cn/"
headers = {
    "Content-Type": "image/png",
    "Authorization": "Basic ZGV2enlodXBsb2FkOnFuTnV2bm9URnhXVzN5dkpJZEpYN0pZNTRNb3hIbnRQ"
}

print("Upload Success:")

for img in img_list:
    file = None

    if img.startswith("http"):
        # 网络图片
        res = requests.get(img, {"User-Agent": "Typora/1.0.0 (https://typora.io)"})
        file = io.BytesIO(res.content)
        img = urlparse(img).path
    else:
        # 本地图片
        file = open(img, "rb")

    # 上传到又拍云
    name = str(uuid.uuid4()).replace("-", "")
    ext = os.path.splitext(img)[1]
    url = "https://v0.api.upyun.com/devzyh-image/" + name + ext
    res = requests.post(url, headers=headers, data=file)

    if len(res.text) == 0:
        print(domain + name + ext)
    else:
        print(res)

    file.close()
