"""
作者：devzyh
日期：2023-07-14
描述：语雀笔记批量导出为Markdown
"""
import json
import os
import shutil
import urllib.parse

import requests

import _export_book

# 语雀Cookie
cookie = ""
# 图片路径前缀
img_url_prefix = "https://img.devzyh.cn/"
# 文件编号长度
seq_len = 3


# 获取知识库列表
def get_books():
    res = requests.get("https://www.yuque.com/api/mine/book_stacks", headers={
        'Cookie': cookie
    })
    books = json.loads(res.text)["data"][0]["books"]
    return books


# 获取目录信息
def get_toc(book):
    res = requests.get("https://www.yuque.com/" + book["user"]["login"] + "/" + book["slug"], headers={
        'Cookie': cookie
    })
    rows = res.text.splitlines()
    app_data = ""
    for row in rows:
        if row.find("window.appData = JSON.parse") == -1:
            continue
        app_data = row.replace("window.appData = JSON.parse(decodeURIComponent(\"", "")
        app_data = app_data.replace("\"));", "")
        app_data = app_data.replace(" ", "")
        break

    if len(app_data) > 0:
        data = urllib.parse.unquote(app_data)
        return json.loads(data)["book"]["toc"]
    else:
        return []


# 程序入口，语雀Cookie必填
if __name__ == "__main__":
    # 接受输入数据

    # 本地图片目录
    img_dir = "output/img"
    if os.path.exists(img_dir):
        shutil.rmtree(path=img_dir)
        print("清空本地图片目录：" + img_dir)
    os.mkdir(img_dir)
    print("创建本地图片目录：" + img_dir)

    # 获取知识库目录
    for book in get_books():
        name = book["name"]
        toc = get_toc(book)

        # 本地知识库目录
        book_dir = "output/" + name
        if os.path.exists(book_dir):
            shutil.rmtree(path=book_dir)
            print("清空本地知识库目录：" + book_dir)
        os.mkdir(book_dir)
        print("创建本地知识库目录：" + book_dir)

        print("开始导出语雀知识库：" + name)
        _export_book.export(book["slug"], toc, book_dir)

    print("知识库导出完毕！")
