"""
工具类
"""

import re


# 下划线转驼峰(小驼峰)
def name_to_camel(name):
    return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)
