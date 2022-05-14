# -*- coding = utf-8 -*-
# @Time:2021/3/30 21:29
# @Author:anonymity
# @File:XwltDemo.py
# @Software:PyCharm

import xlwt

#创建workbook对象
woorkbook = xlwt.Workbook(encoding="utf-8")

#创建工作表
woorsheet = woorkbook.add_sheet('sheet1')

for i in range(0,9):
    for j in range(0,i+1):
        woorsheet.write(i, j, i*j)

woorkbook.save('test.xls')