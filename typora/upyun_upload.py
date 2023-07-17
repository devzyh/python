"""
作者：devzyh
时间：2023-07-14
描述：Typora图片上传又拍云客户端
"""
import http.client
import os
import sys
import uuid

img_list = sys.argv[1:]
domain = "https://img.devzyh.cn/"
bucket = "/devzyh-image/"
headers = {
    "Content-Type": "image/png",
    "Authorization": "Basic ZGV2enlodXBsb2FkOnFuTnV2bm9URnhXVzN5dkpJZEpYN0pZNTRNb3hIbnRQ"
}

print("Upload Success:")
conn = http.client.HTTPSConnection("v0.api.upyun.com")

for img in img_list:
    ext = os.path.splitext(img)[-1]
    name = str(uuid.uuid4()).replace("-", "")
    payload = open(img, "rb")

    conn.request("POST", bucket + name + ext, payload, headers)
    res = conn.getresponse().read().decode("utf-8")

    if len(res) == 0:
        print(domain + name + ext)
    else:
        print(res)

conn.close()
