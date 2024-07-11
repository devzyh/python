"""
作者：devzyh
日期：2024-07-11
描述：周报表格转为邮件
"""
import os

from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

name = "devzyh"
item_split = "@"


# 解析工作表
def parse_sheet(ws: Worksheet) -> map:
    projects = {}
    for row in ws.iter_rows(values_only=True):
        # 只获取指定用户
        if row[7] != name:
            continue

        project_name = row[0]
        project_items = []
        if project_name in projects:
            project_items = projects.get(project_name)
        remarks = row[10]
        if remarks is None:
            remarks = ""
        project_items.append(row[5] + item_split + remarks)

        projects[project_name] = project_items

    return projects


# 输出内容
def print_content(title: str, projects: map):
    print(title + "：")
    for pn in projects:
        print("    " + pn + "：")
        for index, item in enumerate(projects[pn], start=1):
            text = item.split(item_split)
            tb = text[0]
            remarks = text[1]
            if len(remarks) > 0:
                print("        " + str(index) + ". " + tb + "：")
            else:
                print("        " + str(index) + ". " + tb)
                continue
            for r_index, remark in enumerate(remarks.split("\n"), start=1):
                # 目前使用内容自带的序号，不写时替换为变量r_index
                if ". " in remark:
                    print("            " + remark)
                else:
                    print("            " + str(r_index) + ". " + remark)


# 获取文件夹里最新的文件
excel_path = 'excel'
files = sorted(os.listdir(excel_path), key=lambda x: os.path.getmtime(os.path.join(excel_path, x)), reverse=True)
first_file = excel_path + os.sep + files[0]

print("开始提取文件[" + first_file + "]内容")

# 读取excel文件
wb = load_workbook(filename=first_file)

# 总结
projects = parse_sheet(wb.worksheets[1])
print_content("总结", projects)

print("")

# 计划
projects = parse_sheet(wb.worksheets[0])
print_content("计划", projects)
