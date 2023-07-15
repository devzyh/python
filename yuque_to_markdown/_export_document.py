"""
按文档导出
"""
import http.client

# 语雀Cookie
cookie = ""


# 请求语雀
def get_yuque_markdown(book, doc):
    conn = http.client.HTTPSConnection("www.yuque.com")
    headers = {
        'Cookie': cookie,
        'content-type': 'text/markdown'
    }
    conn.request("GET", "/devzyh/" + book + "/" + doc +
                 "/markdown?attachment=true&latexcode=true&anchor=false&linebreak=false",
                 "", headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode("utf-8")


# 转移图片位置
def move_image(data: str):
    return data


# 导出文档
def export(book, doc, local_path):
    f = open(local_path, "w", encoding="utf-8")
    data = get_yuque_markdown(book, doc)
    data = move_image(data)
    f.write(data)
    f.close()
    print("下载语雀文档到：" + local_path)

# 测试 tech cwllhk0xc8nus4mz
