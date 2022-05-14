# -*- coding = utf-8 -*-
# @Time:2021/3/30 21:57
# @Author:anonymity
# @File:SqlLiteDemo.py
# @Software:PyCharm

import sqlite3

#打开或创建数据库文件
conn = sqlite3.connect("test.db")
print("成功打开数据库")

# 获取游标
c = conn.cursor()
#
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real);
# '''
#
# c.execute(sql)

sql = '''
    insert into company 
    values (1,'小明',18,'成都',8000)
'''

c.execute(sql)


conn.commit()
conn.close()
