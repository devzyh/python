"""
按文档导出
"""
import os
import re
import uuid
from urllib.parse import urlparse

import requests

import main


# 请求语雀
def get_markdown(book, doc):
    headers = {
        'Cookie': main.cookie,
        'content-type': 'text/markdown'
    }
    url = "https://www.yuque.com/devzyh/" + book + "/" + doc \
          + "/markdown?attachment=true&latexcode=true&anchor=false&linebreak=false"
    res = requests.get(url, headers=headers)
    return res.text


# 下载语雀图片
def download_image(url: str):
    headers = {
        'User-Agent': 'Python/1.0.0 (https://python.org)',
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    try:
        res = requests.get(url, headers=headers)
    except:
        print("下载图片失败：" + url)
        return url

    file = str(uuid.uuid4()).replace("-", "") + os.path.splitext(urlparse(url).path)[1]
    with open("output/img/" + file, "wb") as f:
        f.write(res.content)

    return main.img_url_prefix + file


# 转移图片
def move_image(data: str):
    # 提取图片
    images = re.findall(r'(?:!\[(.*?)\]\((.*?)\))', data)
    img_map = {}
    for img_info in images:
        img_url = img_info[1]
        # 自适应http协议头处理
        if img_url.startswith("//"):
            img_url = str(img_url).replace("//", "http://")

        # 跳过本地图片
        if not img_url.startswith("http"):
            continue

        # 下载文件
        new_url = download_image(img_url)

        # 写入地址对照
        img_map[img_url] = new_url

    # 替换图片地址
    for map in img_map.keys():
        data = data.replace(map, img_map[map])

    return data


# 导出单个文档
def export(book, doc, local_path):
    f = open(local_path, "w", encoding="utf-8")
    data = get_markdown(book, doc)
    data = move_image(data)
    f.write(data)
    f.close()
    print("下载语雀文档到：" + local_path)
