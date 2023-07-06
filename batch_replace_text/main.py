"""
作者：devzyh
日期：2023-07-06
描述：根据rules文件夹下规则批量替换指定目录文本文件
"""
import os

# 文件选择
dir = input("请输入文本所在目录：")
if not os.path.exists(dir):
    print("目录[" + dir + "]不存在！")
    exit()
files = os.listdir(dir)
if len(files) == 0:
    print("目录[" + dir + "]下不存在文件！")
    exit()

# 规则选择
rules = "./rules"
if not os.path.exists(rules):
    print("替换规则目录[" + rules + "]不存在")
    exit()

rule_files = os.listdir(rules)
rule_files.remove(".gitignore")
rule_files.remove("rule.example.txt")

print("替换规则文件列表")
for idx, val in enumerate(rule_files):
    print("[" + str(idx) + "]" + val)
rules_index = input("请输入规则文件序号：")
rule_path = rules + "/" + rule_files[int(rules_index)]
print("已选择规则文件[" + rule_path + "]")

# 解析替换规则
with open(rule_path, "r", encoding="utf-8") as rf:
    rule_lines = rf.readlines()

rule_map = {}
line_num = 1
map_key = ""
for line in rule_lines:
    line = line.replace("\n", "")
    if len(line) == 0:
        continue

    if line_num % 2 == 0:
        # 替换后文本
        rule_map[map_key] = line
    else:
        # 替换前文本
        rule_map[line] = line
        map_key = line

    line_num = line_num + 1

# 执行内容替换
for file in files:
    file_path = dir + "/" + file
    tmp_file_path = file_path + ".tmp"

    if os.path.isdir(file_path):
        print("目录[" + file_path + "]跳过替换处理！")
        continue

    # 打开替换前文件
    with open(file_path, "r", encoding="utf-8") as rf:
        # 创建替换后文件
        with open(tmp_file_path, "w", encoding="utf-8") as wf:
            # 逐行替换文件内容
            for line in rf.readlines():
                for rule_key in rule_map.keys():
                    line = line.replace(rule_key, rule_map[rule_key])
                # 写入替换完成的内容到临时文件
                wf.write(line)

    # 恢复文件名称
    os.remove(file_path)
    os.rename(tmp_file_path, file_path)
    print("文件[" + file_path + "]内容替换完毕！")

print("目录[" + dir + "]下文件已替换完毕！")
