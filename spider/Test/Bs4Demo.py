# -*- coding = utf-8 -*-
# @Time:2021/3/30 9:09
# @Author:anonymity
# @File:Bs4Demo.py
# @Software:PyCharm
'''
BeautifulSoup4将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象Tl乂归纳为4种;
Tag
Navigablestring
BeautifulSoup
comment
'''

from bs4 import BeautifulSoup

file = open("baidu.html", "rb")
html = file.read().decode("utf-8")
bs= BeautifulSoup(html,"html.parser")
#
# print(bs.title)
# #<class 'bs4.element.Tag'> 获取第一个标签和内容
# print(type(bs.head))
# #<class 'bs4.element.NavigableString'> 标签里的内容
# print(bs.title.string)
# print(type(bs.title.string))
# #attrs获取属性
# print(bs.a.attrs)
#
# print(bs)


#文档的遍历

# print(bs.head.contents[1])


#文档的搜索

#find过滤：查找与字符串完全匹配的内容
# t_list = bs.find_all("a")
# print(t_list)

#正则表达式：使用search()
import re
# t_list = bs.find_all(re.compile("a"))
# print(t_list)


# def name_is_exist(tag):
#     return tag.has_attr("name")


# t_list = bs.find_all(class_=True)
#
# for item in t_list:
#     print(item)


#t_list = bs.find_all(text="hao123")
# t_list = bs.find_all(text= re.compile("\d"))
# for item in t_list:
#     print(item)

#4.limit参数
# t_list = bs.find_all("a",limit=5)
# for item in t_list:
#     print(item)


#选择器
print(bs.select('title'))