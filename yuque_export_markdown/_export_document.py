"""
按文档导出
"""
import http.client
import os
import re
import uuid

import main


# 请求语雀
def get_yuque_markdown(book, doc):
    conn = http.client.HTTPSConnection("www.yuque.com")
    headers = {
        'Cookie': main.cookie,
        'content-type': 'text/markdown'
    }
    conn.request("GET", "/devzyh/" + book + "/" + doc +
                 "/markdown?attachment=true&latexcode=true&anchor=false&linebreak=false",
                 "", headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode("utf-8")


# 下载语雀图片
def download_yuque_image(url: str):
    conn = http.client.HTTPSConnection("cdn.nlark.com")
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        "Accept": "*/*",
        "Host": "cdn.nlark.com",
        "Connection": "keep-alive"
    }
    url = url.replace("https://cdn.nlark.com", "").split("#")[0].split("?")[0]
    conn.request("GET", url, "", headers)
    res = conn.getresponse()
    file = str(uuid.uuid4()).replace("-", "") + os.path.splitext(url)[-1]
    with open("output/img/" + file, "wb") as f:
        f.write(res.read())
    conn.close()

    return main.img_url_prefix + file


# 转移图片位置
def move_image(data: str):
    # 提取图片
    images = re.findall(r'(?:!\[(.*?)\]\((.*?)\))', data)
    img_map = {}
    for img_info in images:
        img_url = img_info[1]

        # 跳过非语雀图片
        if str(img_url).find("cdn.nlark.com") == -1:
            continue

        # 下载文件
        new_url = download_yuque_image(img_url)

        # 写入地址对照
        img_map[img_url] = new_url

    # 替换图片地址
    for map in img_map.keys():
        data = data.replace(map, img_map[map])

    return data


# 导出文档
def export(book, doc, local_path):
    f = open(local_path, "w", encoding="utf-8")
    data = get_yuque_markdown(book, doc)
    data = move_image(data)
    f.write(data)
    f.close()
    print("下载语雀文档到：" + local_path)
