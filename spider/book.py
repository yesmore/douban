# -*- coding = utf-8 -*-

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import sqlite3

# 图书详情
findlink = re.compile(r'<a href="(.*?)"')
#书名
findTitle = re.compile(r'onclick=".*?" title="(.*)">')
#作者
findAuthor =re.compile(r'<p class="pl">(.*?)/')
#图书评分
findNum = re.compile(r'<span class="rating_nums">(.*)</span>')
#评分人数
findJudge = re.compile(r'(\d*)人评价')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')


def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        # 保存获取到的网页源码
        html = askURL(url)
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('tr', class_="item"):
            data = []
            item = str(item)
            link = re.findall(findlink, item)[0]
            data.append(link)
            title = re.findall(findTitle,item)[0]
            data.append(title)
            author = re.findall(findAuthor,item)[0]
            data.append(author)
            score = re.findall(findNum,item)[0]
            data.append(score)
            counts = re.findall(findJudge,item)[0]
            data.append(counts)
            Inq = re.findall(findInq, item)
            if len(Inq) > 0:
                    data.append(""+Inq[0])
            else:
                    data.append(' ')
            # bd = re.findall(findBd,item)[0]
            # bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            # data.append("".join(bd.split()))
            datalist.append(data)
    return datalist


def main():
    baseurl = "https://book.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    dbpath = "../web_server/douban.db"
    saveDataDB(datalist, dbpath)

def init_db(dbpath):
    sql = '''
    create table book  (
         id INTEGER primary key autoincrement,
         link_src text not null,
         title varchar ,
         author varchar ,
         score numeric ,
         rated numeric ,
         inp text);
    '''
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def saveDataDB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    for data in datalist:
        for index in range(0,len(data)):
            if  index ==3 or index ==4:
                continue
            data[index] = '"'+data[index]+'"'

        sql = '''                       
                 insert into book(
                 link_src,title,author,score,rated,inp
                 )values(%s)
                    ''' % ",".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()

def askURL(Url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0}"
    }
    request = urllib.request.Request(url=Url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

if __name__ == '__main__':
    main()
