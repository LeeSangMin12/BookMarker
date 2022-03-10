from flask import Flask, render_template, jsonify, request, redirect, url_for
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
import requests
import jwt
import hashlib
import datetime
app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.d1kjh.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.bookmaker
SECRET_KEY = 'sparta'
# import detail
# import login

# app.register_blueprint(detail.detail_blueprint)
# app.register_blueprint(login.login_blueprint)

###################################################
# app.py
###################################################
@app.route("/")
def home():
    token = request.cookies.get('mytoken')

    return render_template("index.html", str=token)


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
    bookSum = soup.select_one('#tabimage2').contents

    bookNum = soup.select_one(
        '#productView > div.productArea.product-area > div > dl > dt > div.btnPreview > form > input[type=hidden]:nth-child(2)')[
        'value']
    bookPublisher = soup.select_one('#book_desc_mid > dd.mT10.prodInfo-dd > a:nth-child(2) > strong').text

    doc = {
        'bookTitle': bookTitle,
        'bookUrl': bookUrl,
        'bookAuthor': bookAuthor,
        'bookPublisher': bookPublisher,
        'bookSum': 1,
        'bookNum': bookNum
    }
    db.books.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/getBookInfor", methods=["POST"])
def get_book_infor():
    url_receive = request.form['url_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    title_test = soup.select_one('#book_desc_mid > dd.bookNameTitle').text
    bookTitle = title_test.replace("소득공제", "").strip()
    bookUrl = soup.select_one('#book_img')['src']
    bookAuthor = soup.select_one('#book_desc_mid > dd.mT10.prodInfo-dd > a:nth-child(1) > strong').text

    show_book = {
        'bookTitle': bookTitle,
        'bookUrl': bookUrl,
        'bookAuthor': bookAuthor
    }

    return jsonify({'showBook': show_book})


@app.route("/listBook", methods=["GET"])
def book_get():
    book_list = list(db.books.find({}, {'_id': False}))
    return jsonify({'books': book_list})


@app.route("/upload")
def upload():
    return render_template("upload.html", urlChk="False")

###################################################
# detail.py
###################################################


@app.route("/detail/detail/<keyword>")
def detail(keyword):

    book = db.books.find_one({'bookNum': keyword})
    paragraph = list(db.paragraph.find({'bookNum': keyword},{}))
    return render_template("detail/detail.html", book=book, paragraph=paragraph,)


# 코멘트 작성
@app.route("/detail/write_paragraph", methods=["POST"])
def write_paragraph():
    if chk_user_login() is True:
        book_num = request.form.get('bookNum')
        para_content = request.form.get('paraContent')
        write_date = request.form.get('writeDate')
        max_para_num = db.paragraph.find_one(sort=[("paraNum", -1)])
        new_para_num = int(max_para_num['paraNum'])+1

        paragrpah = {
            'bookNum': book_num,
            'paraNum': new_para_num,
            'userId': token_get_userinfo()['userId'],
            'paraContent': para_content,
            'writeDate': write_date
        }
        db.paragraph.insert_one(paragrpah)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result' : 'fail','msg':chk_user_login()})


@app.route("/detail/delete_paragraph", methods=['POST'])
def delete_paragraph():
    if chk_user_login() is True:
        para_num = request.form.get('paraNum')
        writer = db.user.find_one({'paraNum': para_num})
        print(type(writer['userId']))
        print(type(token_get_userinfo()['userId']))
        if writer['userId'] == token_get_userinfo()['userId']:
            db.paragraph.delete_one({'paraNum': int(para_num)})
            return jsonify({'result': 'success','msg':'삭제!'})
        else:
            return jsonify({'result': 'fail', 'msg': '권한이 없습니다.'})
    else:
        return jsonify({'result': 'fail','msg':'권한이 없습니다.'})

###################################################
# login.py
###################################################

@app.route("/login/login")
def login():
    return render_template("login/login.html")


@app.route("/login/rgstr")
def rgstr():
    return render_template("login/rgstr.html")


@app.route("/login/userRgstr", methods=['POST'])
def user_rgstr():
    user_name = request.form['userName']
    user_id = request.form['userId']
    user_pwd = request.form['userPwd']

    # 비밀번호 암호화
    pw_hash = hashlib.sha256(user_pwd.encode('utf-8')).hexdigest()

    db.user.insert_one({'userName': user_name, 'userId': user_id, 'userPwd': pw_hash})

    return jsonify({'result': 'success'})


@app.route("/login/userLogin", methods=['POST'])
def user_login():
    user_id = request.form['userId']
    user_pwd = request.form['userPwd']
    # # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(user_pwd.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'userId': user_id, 'userPwd': pw_hash})
    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'userName': result['userName'],
            'userId' : user_id,
            'userPwd': pw_hash,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


def token_decode():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    return payload


def token_get_userinfo():
    payload = token_decode()
    result = db.user.find_one({'userId': payload['userId'], 'userPwd': payload['userPwd']})
    return result


def chk_user_login():
    try:
        payload = token_decode()
        print(payload)
        return True
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return "로그인 시간이 만료되었습니다"
    except jwt.exceptions.DecodeError:
        return "로그인 정보가 존재하지 않습니다."




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
