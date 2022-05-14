# -*- coding = utf-8 -*-

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import xlwt
import sqlite3


findlink = re.compile(r'<a href="(.*?)">')  # 影片详情
findImgSrc = re.compile(r'<img .*src="(.*?)"', re.S)  # 影片图片 re.S让换行符包含
findTitle = re.compile(r'<span class="title">(.*)</span>')  # 影片片名
findNum = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  # 影片评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')  # 评分人数
findInq = re.compile(r'<span class="inq">(.*)</span>')  # 找到概况
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)  # 找到影片相关内容


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = ".\\Top250.xls"
    dbpath = "../web_server/douban.db"
    saveData(datalist, savepath)
    saveDataDB(datalist, dbpath)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        # 保存获取到的网页源码
        html = askURL(url)
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)
            link = re.findall(findlink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            title = re.findall(findTitle, item)
            data.append(title[0])
            if len(title) > 1:
                title[1] = ("".join(title[1].split())).replace("/","")
                data.append(title[1])
            else:
                data.append(' ')
            num = re.findall(findNum, item)[0]
            data.append(num)
            judge = re.findall(findJudge, item)[0]
            data.append(judge)
            Inq = re.findall(findInq, item)
            if len(Inq)>0:
                data.append(Inq[0])
            else:
                data.append(' ')
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            data.append("".join(bd.split()))

            datalist.append(data)
    return datalist


# 得到指定URL的网页内容
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


def saveData(datalist, depath):
    wookbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
    wooksheet = wookbook.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)
    col = ('电影链接', "图片链接", "影片中文名","影片原名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        wooksheet.write(0, i, col[i])
    for i in range(0,250):
        data = datalist[i]
        for j in range (0,8):
            wooksheet.write(i+1,j,data[j])
    wookbook.save(depath)


def saveDataDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if  index ==4 or index ==5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''                       
                        insert into movie(
                        link_src,pic_src,ctitle,otitle,score,rated,inp,info
                        )values(%s)
                    ''' % ",".join(data)
        print(",".join(data))
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


def init_db(dbpath):
    sql = '''
    create table movie  (
         id INTEGER primary key autoincrement,
         link_src text not null,
         pic_src text not null,
         ctitle varchar ,
         otitle varchar ,
         score numeric ,
         rated numeric ,
         inp text,
         info text);
    '''
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
