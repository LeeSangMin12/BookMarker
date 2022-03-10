from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import certifi
from login import token_get_userinfo, chk_user_login

detail_blueprint = Blueprint("detail", __name__, url_prefix="/detail")

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.d1kjh.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.bookmaker


@detail_blueprint.route("/detail/<keyword>")
def detail(keyword):

    book = db.books.find_one({'bookNum': keyword})
    paragraph = list(db.paragraph.find({'bookNum': keyword},{}))
    return render_template("detail/detail.html", book=book, paragraph=paragraph,)


# 코멘트 작성
@detail_blueprint.route("/write_paragraph", methods=["POST"])
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


@detail_blueprint.route("/delete_paragraph", methods=['POST'])
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







