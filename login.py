from flask import Blueprint, render_template, request, jsonify, Response
from pymongo import MongoClient
import certifi

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
from app import SECRET_KEY

login_blueprint = Blueprint("login", __name__, url_prefix="/login")

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.d1kjh.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.bookmaker


@login_blueprint.route("/login")
def login():
    return render_template("login/login.html")


@login_blueprint.route("/rgstr")
def rgstr():
    return render_template("login/rgstr.html")


@login_blueprint.route("/deleteCookies", methods=['POST'])
def user_rgstr():
    user_name = request.form['userName']
    user_id = request.form['userId']
    user_pwd = request.form['userPwd']

    # 비밀번호 암호화
    pw_hash = hashlib.sha256(user_pwd.encode('utf-8')).hexdigest()

    db.user.insert_one({'userName': user_name, 'userId': user_id, 'userPwd': pw_hash})

    return jsonify({'result': 'success'})


@login_blueprint.route("/userLogin", methods=['POST'])
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
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

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
