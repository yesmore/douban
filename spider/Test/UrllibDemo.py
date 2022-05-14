# -*- coding = utf-8 -*-
# @Time:2021/3/29 23:42
# @Author:anonymity
# @File:UrllibDemo.py
# @Software:PyCharm

import urllib.request

#获取一个get请求
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode("utf-8"))


#获取一个post请求

import urllib.parse
# data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response1 = urllib.request.urlopen("http://httpbin.org/post",data=data)
# print(response1.read().decode("utf-8"))


# import urllib.error
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get",timeout=0.01)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as e:
#     print("超时了")

#测试状态码
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.status)
# print(response.getheaders())
# print(response.getheader("Server"))

#测试模拟请求头
# headers={
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
# }
#
# url = "http://httpbin.org/post"
# data = bytes(urllib.parse.urlencode({ "hello":"world"}),encoding="utf-8")
# request = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
# response = urllib.request.urlopen(request)
# print(response.read().decode("utf-8"))


#
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
}
url = "https://www.baidu.com"
request= urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(request)
print(response.read().decode("utf-8"))