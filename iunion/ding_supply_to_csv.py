"""
作者：devzyh
版本：v1.0.0
描述：转换九格合众钉钉群签到供应商数据为CSV
"""
import os

# 本次提取变量
file_path = "file/20230423.txt"  # 文件名称
check_date = "20230423"  # 签到日期
salesperson = "欧阳俊杰"  # 销售人员
is_kp = "是"  # 是否KP

# 文件存在验证
if not os.path.exists(file_path):
    print("文件[" + file_path + "]不存在！")
    exit()

# 读取文件
with open(file_path, "r", encoding="utf-8") as rf:
    txt = rf.read()

# 键值对齐
txt = txt + "\n00:00今日结束"
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
initMap = {
    "company": "",
    "address": "",
    "phone": "",
    "wechat": "",
    "device": "",
    "qty": "",
    "operator": ""
}
map = initMap.copy()
for line in txt.splitlines():
    words = line.split("@")
    key = words[0].strip()
    if len(words) > 1:
        val = words[1].strip()

    # 公司名称
    if "公司名称" == key:
        map["company"] = val
        continue

    # 公司地址
    if "公司位置" == key:
        map["address"] = val
        continue

    # 联系方式
    if "备注" == key:
        map["phone"] = val
        continue

    # 是否添加微信
    if "是否添加微信" == key:
        map["wechat"] = val
        continue

    # 主营设备
    if "设备类型" == key:
        val = val.replace("\"", "").replace("[", "").replace("]", "").replace(",", "、")
        map["device"] = val
        continue

    # 吨位、高度、型号
    if "吨位、高度、型号" == key:
        map["device"] = map["device"] + " " + val
        continue

    # 设备数量
    if "设备数量" == key:
        map["qty"] = val
        continue

    # 是否有机手
    if "是否有机手" == key:
        map["operator"] = val
        continue

    # 一条次签到结束
    if ":" == key[2]:
        # CSV格式
        row = check_date + "," + salesperson + "," + map["company"] + "," + map["address"] + "," + is_kp + "," + \
              map["phone"] + "," + map["wechat"] + "," + map["device"] + "," + map["qty"] + "," + map["operator"]

        rows.append(row)
        map = initMap.copy()

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
