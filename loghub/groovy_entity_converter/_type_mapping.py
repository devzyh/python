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
    java = java.lower()
    if java in "integer,long":
        return "bigint(20)"
    elif java in "string":
        return "varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci"
    elif java in "float,double,bigdecimal":
        return "decimal(15, 6)"
    elif java in "date":
        return "date"
    elif java in "datetime,localdatetime":
        return "datetime"
    else:
        return java
