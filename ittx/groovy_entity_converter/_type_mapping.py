"""
数据类型转换文件
"""


# Java类型转换JS类型
def java_to_js(java: str):
    java = java.lower()
    if java in "integer":
        return "integer"
    elif java in "string":
        return "string"
    elif java in "long,float,double,bigdecimal":
        return "number"
    elif java in "localdatetime":
        return "datetime"
    else:
        return java


# Java类型转换MySQL类型
def java_to_mysql(java):
    return "mysql" + java
