from flask import Flask, render_template
import sqlite3
import jieba
from wordcloud import WordCloud

app = Flask(__name__)
# 支持热更新
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def score():
    scores = []
    counts = []
    conn = sqlite3.connect("douban.db")
    cursor = conn.cursor()
    sql = '''
    select score,count(score) from movie group by score
    '''
    data = cursor.execute(sql)
    for item in data:
        scores.append(item[0])
        counts.append(item[1])
    sql1 = '''
    select score,count(score),sum(rated) from book group by score
    '''
    data = cursor.execute(sql1)
    book_socre = []
    book_count = []
    book_rated = []
    for item in data:
        book_socre.append(item[0])
        book_count.append(item[1])
        book_rated.append(item[2])
    cursor.close()
    conn.close()
    [score_num, words] = total_data()
    return render_template("score.html", score_num=score_num, words=words, scores=scores, counts=counts,book_socre=book_socre,book_count=book_count,book_rated=book_rated)


def total_data():
    conn = sqlite3.connect('douban.db')
    cursor = conn.cursor()
    sql = '''
    select sum(rated) from movie;
    '''

    data = cursor.execute(sql)
    for item in data:
        count = item[0]
        break
    sql = '''
    select sum(rated) from book;
    '''
    data = cursor.execute(sql)
    for item in data:
        count += item[0]
        break


    sql = '''
        select inp from book
    '''
    data = cursor.execute(sql)
    text = ""
    for item in data:
        text = text + item[0]
    sql = '''
        select inp from movie
    '''
    data = cursor.execute(sql)
    text = ""
    for item in data:
        text = text + item[0]

    cursor.close()
    cursor.close()

    cut = jieba.cut(text)
    global wc_data
    wc_data = ' '.join(cut)
    wc_data = filter_wc(wc_data)
    words = len(wc_data)
    cursor.close()
    conn.close()
    count = round(count / 10000)
    # 模板渲染
    return [count, words]


@app.route('/movie')
def movie():
    datalist = []
    conn = sqlite3.connect("douban.db")
    cur = conn.cursor()
    sql = '''
    select * from movie
    '''
    data = cur.execute(sql)

    for item in data:
        datalist.append(list(item))
    cur.close()
    conn.close()
    return render_template("movie.html", movies=datalist)


@app.route('/book')
def book():
    datalist = []
    conn = sqlite3.connect("douban.db")
    cur = conn.cursor()
    sql = '''
    select * from book
    '''
    data = cur.execute(sql)
    print(data)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()

    return render_template("book.html", books=datalist)


@app.route('/word')
def wc_generater():
    [score_num, words] = total_data()
    wc = WordCloud(  # 设置参数
        font_path=r'C:\Windows\Fonts\STSONG.ttf',  # 设置字体路径
        width=1000,
        height=1000,
        background_color='black'
    )
    # print(wc_data)
    wc.generate(wc_data)  # 生产词云
    wc.to_file('./static/assets/img/movie.jpg')
    return render_template("word.html", words=words)


def filter_wc(wc_data):
    print('词集：')
    # 过滤词
    rb = ['的', '是', '你', '我', '她', '了', '就', '都', '没有', '们', '不', '在']
    for i in range(len(rb)):
        wc_data = wc_data.replace(rb[i], '')
    return wc_data


if __name__ == '__main__':
    app.run(port=3000)
