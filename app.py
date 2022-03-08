from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import detail
import login

url = 'https://www.ypbooks.co.kr/book.yp?bookcd=101155172'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

title_test = soup.select_one('#book_desc_mid > dd.bookNameTitle').text
title = title_test.replace("소득공제","").strip()

image = soup.select_one('#book_img')['src']

author = soup.select_one('#book_desc_mid > dd.mT10.prodInfo-dd > a:nth-child(1) > strong').text

sum = soup.find_all('#leftArea02 > div.entire_wrap > div.bookInfo > div:nth-child(6)')

publisher = soup.select_one('#book_desc_mid > dd.mT10.prodInfo-dd > a:nth-child(2) > strong').text
print(publisher)

app = Flask(__name__)

# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:sparta@cluster0.lafvq.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.bookmaker
#
# db.users.insert_one({'name' : 'bob'})

app.register_blueprint(login.login_blueprint)
app.register_blueprint(detail.detail_blueprint)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_post():
    doc = {
        'title':title,
        'image':image,
        'desc':desc,
        'star':star_receive,
        'comment':comment_receive
    }
    db.movies.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/upload")
def upload():
    return render_template("upload.html", urlChk="False")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
