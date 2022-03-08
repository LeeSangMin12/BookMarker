from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
import requests
import detail
import login

app = Flask(__name__)


ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.lafvq.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.bookmaker
#
# db.users.insert_one({'name' : 'bob'})

app.register_blueprint(login.login_blueprint)
app.register_blueprint(detail.detail_blueprint)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_post():
    url_receive = request.form['url_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title_test = soup.select_one('#book_desc_mid > dd.bookNameTitle').text
    bookTitle = title_test.replace("소득공제", "").strip()
    bookUrl = soup.select_one('#book_img')['src']
    bookAuthor = soup.select_one('#book_desc_mid > dd.mT10.prodInfo-dd > a:nth-child(1) > strong').text
    # bookSum = soup.select_one('#tabimage2').contents
    bookSum = 1
    bookNum = soup.select_one('#productView > div.productArea.product-area > div > dl > dt > div.btnPreview > form > input[type=hidden]:nth-child(2)')['value']
    bookPublisher = soup.select_one('#book_desc_mid > dd.mT10.prodInfo-dd > a:nth-child(2) > strong').text

    doc = {
        'bookTitle':bookTitle,
        'bookUrl':bookUrl,
        'bookAuthor':bookAuthor,
        'bookPublisher':bookPublisher,
        'bookSum': bookSum,
        'bookNum': bookNum
    }
    db.books.insert_one(doc)

    return jsonify({'msg':'등록 완료!'})

@app.route("/listBook", methods = ["GET"])
def book_get():
    book_list = list(db.books.find({},{'_id':False}))
    return jsonify({'books':book_list})

@app.route("/upload")
def upload():
    return render_template("upload.html", urlChk="False")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
