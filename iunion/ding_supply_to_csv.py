"""
作者：devzyh
版本：v1.1.0
描述：转换九格合众钉钉群签到供应商数据为CSV
"""
import os

# 本次提取变量
check_date = "20230506"  # 签到日期
salesperson = "销售人员"  # 销售人员
is_kp = "是"  # 是否KP

# 文件存在验证
file_path = "file/" + check_date + ".txt"
if not os.path.exists(file_path):
    print("文件[" + file_path + "]不存在！")
    exit()

# 读取文件
with open(file_path, "r", encoding="utf-8") as rf:
    txt = rf.read()

# 去除无效数据及键值同行
if txt.find("今日\n签到") > -1:
    txt = txt.split("今日\n签到")[1]
txt = txt + "\n23:59今日数据结束"
txt = txt.replace("签到地点\n", "签到地点@")
txt = txt.replace("备注\n", "备注@")
txt = txt.replace("签到图片\n", "签到图片@\n")
txt = txt.replace("公司名称：\n", "公司名称@")
txt = txt.replace("公司位置\n", "公司位置@")
txt = txt.replace("设备类型\n", "设备类型@")
txt = txt.replace("吨位、高度、型号\n", "吨位、高度、型号@")
txt = txt.replace("设备数量\n", "设备数量@")
txt = txt.replace("是否添加微信\n", "是否添加微信@")
txt = txt.replace("是否有机手\n", "是否有机手@")
txt = txt.replace("工作区域\n", "工作区域@")

# 循环处理每一行数据
rows = []
phones = set()
repeat_phones = []
default_data = {
    "time": "",
    "company": "",
    "address": "",
    "phone": "",
    "wechat": "",
    "device": "",
    "qty": "",
    "operator": "",
    "area": ""
}
data = default_data.copy()
for line in txt.splitlines():

    # 获取本次签到时间，并记录上一条签到数据
    if len(line) > 2 and ":" == line[2]:
        # 签到时间
        data["time"] = line

        # 上一条签到数据
        if data["phone"] != "":
            # 重复验证
            if data["phone"] in phones:
                repeat_phones.append(data["phone"])
            else:
                # CSV格式
                row = check_date + "," + salesperson + "," + data["company"] + "," + data[
                    "address"] + "," + is_kp + "," + \
                      data["phone"] + "," + data["wechat"] + "," + data["device"] + "," + data["qty"] + "," + data[
                          "operator"]
                rows.append(row)
                phones.add(data["phone"])
                data = default_data.copy()

        continue

    # 提取键值
    words = line.split("@")
    key = words[0].strip()
    val = ""
    if len(words) > 1:
        val = words[1].strip()

    # 公司名称
    if "公司名称" == key:
        data["company"] = val
        continue

    # 公司地址
    if "公司位置" == key:
        data["address"] = val
        continue

    # 联系方式
    if "备注" == key:
        data["phone"] = val
        continue

    # 是否添加微信
    if "是否添加微信" == key:
        data["wechat"] = val
        continue

    # 主营设备
    if "设备类型" == key:
        val = val.replace("\"", "").replace("[", "").replace("]", "").replace(",", "、")
        data["device"] = val
        continue

    # 吨位、高度、型号
    if "吨位、高度、型号" == key:
        data["device"] = data["device"] + " " + val
        continue

    # 设备数量
    if "设备数量" == key:
        data["qty"] = val
        continue

    # 是否有机手
    if "是否有机手" == key:
        data["operator"] = val
        continue

    # 工作区域
    if "工作区域" == key:
        data["area"] = val
        continue

# 输出到CSV文件
# 反向输出
rows.reverse()
# 表格标题
rows.insert(0, "日期,销售姓名,公司名称,公司地址,是否KP,联系方式,是否添加微信,主营设备,设备数量,是否有机手")
csv_path = "file/" + check_date + ".csv"
with open(csv_path, 'w', encoding='utf-8') as wf:
    wf.write("\n".join(rows))

print("提取成功，输出CSV文件到：", csv_path)
print(">>>>>>注意：生成内容仅做参考，具体使用请根据实际情况调整。<<<<<<")
# 重复号码
if len(repeat_phones) > 0:
    print("\n数据重复号码如下：\n" + "\n".join(repeat_phones))
