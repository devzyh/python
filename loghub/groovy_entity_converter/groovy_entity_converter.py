"""
作者：devzyh
日期：2022-12-06
描述：转换Groovy的Entity内容为Creator可以使用的表模型数据
"""
import json
import os
import re

import _type_mapping
import _util

name = input("请输Groovy文件名：")
name = name.replace(".groovy", "")
if len(name) == 0:
    name = "input"
file_path = "groovy/" + name + ".groovy"

if not os.path.exists(file_path):
    print("文件[" + file_path + "]不存在！")
    exit()

# 读取文件
with open(file_path, "r", encoding="utf-8") as rf:
    groovy = rf.read()

# 循环处理每一行代码
table = ""  # 表名称
id_name = ""  # ID列名称
is_meta = False  # 处理元信息
is_prop = False  # 处理属性
tm_fields = []  # 表模型字段数据
ms_fields = []  # 数据库字段数据
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
        js_type = _type_mapping.java_to_js(words[0])
        sql_type = _type_mapping.java_to_mysql(words[0])

        # 获取字段
        p_name = words[1]

        # 获取注释
        p_desc = ""
        if len(words) > 3:
            p_desc = words[3]
        if len(p_desc) == 0:
            p_desc = p_name

        # 组装表模型字段
        tm_field = '{"field":"' + p_name + '","id":"' + p_name + '","name":"' + p_desc + '","type":"' + js_type + '"}'
        tm_fields.append(tm_field)

        # 组装MySql脚本
        if id_name == p_name:
            ms_null = 'NOT NULL AUTO_INCREMENT'
        else:
            ms_null = 'NULL'

        # CBT字段类型处理
        if p_name == "created":
            ms_null = "NULL DEFAULT CURRENT_TIMESTAMP"
            sql_type = "timestamp"
        if p_name == "lastUpdated":
            ms_null = "NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
            sql_type = "timestamp"

        ms_field = '  `' + p_name + '` ' + sql_type + ' ' + ms_null + ' COMMENT \'' + p_desc + '\''
        ms_fields.append(ms_field)

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
json_path = "groovy/" + name + ".tableModel.json"
with open(json_path, 'w', encoding='utf-8') as wf:
    wf.write(json.dumps(json.loads(table_model), indent=2, ensure_ascii=False))
print("转换成功，输出表模型到文件：", json_path)

# 输出MySQL脚本
sql_script = '''DROP TABLE IF EXISTS `@table@`;
CREATE TABLE `@table@` (
@msFields@,
  PRIMARY KEY (`@idName@`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '表名称注释' ROW_FORMAT = Dynamic;
'''
sql_script = sql_script.replace("@idName@", id_name)
sql_script = sql_script.replace("@table@", table)
sql_script = sql_script.replace("@msFields@", ",\n".join(ms_fields))
sql_path = "groovy/" + name + ".sql"
with open(sql_path, 'w', encoding='utf-8') as wf:
    wf.write(sql_script)
print("转换成功，输出表模型到文件：", sql_path)
print(">>>>>>注意：生成内容仅做参考，具体使用请根据实际情况调整。<<<<<<")
