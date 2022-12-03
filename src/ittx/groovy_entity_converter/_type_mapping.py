"""
数据类型转换文件
"""


# Java类型转换JS类型
def java_to_js(java: str):
    java = java.lower()
    if "integer".find(java) != -1:
        return "integer"
    elif "string".find(java) != -1:
        return "string"
    elif "long,float,double,bigdecimal".find(java) != -1:
        return "number"
    elif "localdatetime".find(java) != -1:
        return "datetime"
    else:
        return java


# Java类型转换MySQL类型
def java_to_mysql(java):
    return "mysql" + java
