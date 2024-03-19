"""
作者：devzyh
日期：2024-03-19
描述：提取TB号
"""
import os

import re

name = input("请输input文件夹下文件名（默认input）：\n")
name = name.replace(".groovy", "")
if len(name) == 0:
    name = "input"
file_path = "input/" + name + ".txt"

if not os.path.exists(file_path):
    print("文件[" + file_path + "]不存在！")
    exit()

# 读取文件
with open(file_path, "r", encoding="utf-8") as rf:
    text = rf.read()

# 定义正则表达式模式，匹配带中括号的内容行
pattern = r'\[([^]]+)\]'

# 使用 re.findall 函数查找所有匹配的内容行
matches = re.findall(pattern, text)

print(">>>>>>以下输出是去重并排序后的结果<<<<<<")
for content in sorted(set(matches)):
    print(content)
