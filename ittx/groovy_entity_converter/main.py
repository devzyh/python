"""
作者：devzyh
版本：v1.0.0
描述：转换通天晓Groovy的Entity内容为Creator可以使用的表模型数据
"""
import os
import re

import _type_mapping
import _util

name = input("请输Groovy文件名：")
filePath = "groovy/" + name.replace(".groovy", "") + ".groovy"

if not os.path.exists(filePath):
    print("文件[" + filePath + "]不存在！")
    exit()

# 读取文件
with open(filePath, "r", encoding="utf-8") as rf:
    groovy = rf.read()

# 循环处理每一行代码
table = ""  # 表名称
id_name = ""  # ID列名称
is_meta = False  # 处理元信息
is_prop = False  # 处理属性
tm_fields = []  # 表模型字段数据
for line in groovy.splitlines():
    # 元数据提取判断
    if line.find("define") != -1:
        is_meta = True
        continue

    if is_meta and line.find(")") != -1:
        is_meta = False
        is_prop = True
        continue

    # 字段提取判断
    if is_prop and line.find("@Override") != -1:
        is_prop = False
        continue

    if (not is_prop) and line.find("}") != -1:
        is_prop = True
        continue

    # 提取元信息
    if is_meta:
        str_quota = re.compile(r"'(.*)'")
        if line.find("table") != -1:  # 获取表名称
            table = str_quota.findall(line)[0]
        if line.find("idColumn") != -1:  # 获取ID名称
            id_name = str_quota.findall(line)[0]

    # 提取字段信息
    if is_prop and len(line) > 0:
        line = line.replace(";", "")
        words = line.strip().split()
        # 低于两个单词的行为无效行
        if len(words) < 2:
            continue

        # 获取类型
        jsType = _type_mapping.java_to_js(words[0])

        # 获取字段
        pName = words[1]

        # 获取注释
        pDesc = ""
        if len(words) > 3:
            pDesc = words[3]
        if len(pDesc) == 0:
            pDesc = pName

        # 组装表模型字段
        tm_field = '{"field":"' + pName + '","id":"' + pName + '","name":"' + pDesc + '","type":"' + jsType + '"}'
        tm_fields.append(tm_field)

        # 组装MySql脚本

# 输出表模型
table_model = '''{
  "autoIncrementField": "@idName@",
  "code": "@table@",
  "description": "",
  "fields": [@tmFields@],
  "idColumnName": "@idName@",
  "logHistory": true,
  "service": "@service@",
  "tableName": "@table@"
}'''
table_model = table_model.replace("@idName@", id_name)
table_model = table_model.replace("@table@", table)
table_model = table_model.replace("@service@", _util.name_to_camel(table))
table_model = table_model.replace("@tmFields@", ",".join(tm_fields))
jsonPath = "groovy/" + name + ".tableModel.json"
with open(jsonPath, 'w', encoding='utf-8') as wf:
    wf.write(table_model)
print("转换成功，输出表模型到文件：", jsonPath)

# 输出MySQL脚本
