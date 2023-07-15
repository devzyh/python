"""
作者：devzyh
日期：2023-07-14
描述：语雀笔记导出到Markdown文件
"""
import json
import os
import shutil

import yaml

import _export_book
import _export_document


# 获取目录信息
def get_toc(meta_file):
    f = open(meta_file, "r", encoding="utf-8")
    m = json.loads(f.read())
    f.close()

    m = json.loads(m["meta"])
    toc = m["book"]["tocYml"]

    # 解析知识库标识
    book = m["book"]["path"]
    book = book.split("/")[-1]

    # 解析文档列表
    yml_file = meta_file.replace(".json", ".yml")
    f = open(yml_file, "w", encoding="utf-8")
    f.write(toc)
    f.close()
    toc = yaml.full_load(toc)

    # 屏蔽掉YML的时间格式
    for t in toc:
        t["last_updated_at"] = ""
    toc = toc[1:]
    print(json.dumps(toc))

    return book, toc


# 程序入口，务必填写语雀Cookie
_export_document.cookie = ""

metas = os.listdir("meta")
for meta in metas:
    if not meta.endswith(".json"):
        continue

    # if meta.find("软件技术") == -1:
    #     continue

    print("开始导出语雀知识库：" + meta)
    book, toc = get_toc("meta/" + meta)
    md_dir = "output/" + meta.replace(".json", "")
    if os.path.exists(md_dir):
        shutil.rmtree(path=md_dir)
    os.mkdir(md_dir)
    _export_book.export(book, toc, md_dir)
