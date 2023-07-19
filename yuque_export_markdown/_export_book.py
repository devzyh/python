"""
按知识库导出
"""

import os

import _export_doc
import yuque_export_markdown


# 获取名称前缀
def get_prefix(num):
    return str(num).rjust(yuque_export_markdown.seq_len, "0") + "-"


# 处理标题字符
def remove_special_char(input: str):
    input = input.replace(" ", "")
    input = input.replace("\\", "")
    input = input.replace("/", "")
    input = input.replace(":", "")
    input = input.replace("*", "")
    input = input.replace("?", "")
    input = input.replace("？", "")
    input = input.replace("/\"", "")
    input = input.replace("“", "")
    input = input.replace("”", "")
    input = input.replace("!", "")
    input = input.replace("！", "")
    input = input.replace("、", "")
    return input


# 导出单个知识库
def export(book, toc, book_dir):
    dirs = [book_dir]
    dirs_num = {}
    next_t_index = 0

    for t in toc:
        next_t_index += 1
        title = remove_special_char(t["title"])
        doc_id = str(t["doc_id"])

        # 目录编号数字
        path = str.join("/", dirs)
        if path in dirs_num:
            dirs_num[path] += 1
        else:
            dirs_num[path] = 1
        title = get_prefix(dirs_num[path]) + title

        # 构建本地目录和文件
        if len(doc_id) == 0:
            # 创建目录
            dirs.append(title)
            path = str.join("/", dirs)
            if not os.path.exists(path):
                os.mkdir(path)
                print("创建文件夹：" + path)

            # 空目录直接退出
            if len(t["child_uuid"]) == 0 and next_t_index < len(toc):
                i = 0
                while i <= t["level"] - toc[next_t_index]["level"]:
                    dirs.pop()
                    i += 1


        else:

            # 导出文件
            path = path + "/" + title + ".md"
            _export_doc.export(book, t["url"], path)

            # 本目录最后一个文档导出后切回上一级
            last_doc = len(t["sibling_uuid"]) == 0
            if last_doc and next_t_index < len(toc):
                i = 0
                while i < t["level"] - toc[next_t_index]["level"]:
                    dirs.pop()
                    i += 1
