"""
作者：devzyh
日期：2024-05-20
描述：提取更新日志
"""

import json
import os

import re

base_path = "csv/"
file_path = base_path + "input.csv"

if not os.path.exists(file_path):
    print("文件[" + file_path + "]不存在！")
    exit()

# 读取文件
with open(file_path, "r", encoding="utf-8-sig") as rf:
    text = rf.read()

# 版本号
major_version = 3
minor_version = 0
revision_version = 0
items_date = ""
items = []
versions = []
for line in text.splitlines():
    row = line.split(",")
    row_date = row[0].strip().replace("/", "-")
    row_item = row[1].strip()

    # 初始化日期
    if len(items_date) == 0:
        items_date = row_date

    if row_date != items_date:
        # 记录当前版本数据
        version = {}
        version["version"] = (
            "v"
            + str(major_version)
            + "."
            + str(minor_version)
            + "."
            + str(revision_version)
        )
        version["date"] = items_date
        version["items"] = items
        versions.append(version)

        # 准备记录下一版本数据
        revision_version = revision_version + 1
        items_date = row_date
        items = []

    if row_date == items_date:
        items.append(row_item)

# 反转顺序
versions.reverse()

with open(base_path + "output.json", "w", encoding="utf-8") as wf:
    wf.write(json.dumps(versions, ensure_ascii=False))
