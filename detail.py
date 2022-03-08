from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import certifi
detail_blueprint = Blueprint("detail", __name__, url_prefix="/detail")

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.lafvq.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
mongo_db = client.bookmaker


@detail_blueprint.route("/detail")
def detail():
    return render_template("detail/detail.html", str="detail 나와요?")


# 코멘트 작성
@detail_blueprint.route("/write_paragraph", methods=["POST"])
def write_paragraph():
    if request.method == 'POST':
        book_num = request.form.get('bookNum')
        para_num = request.form.get('paraNum')
        user_id = request.form.get('userId')
        para_content = request.form.get('paraContent')
        write_date = request.form.get('writeDate')

        paragrpah = {
            'bookNum': book_num,
            'paraNum': para_num,
            'userId': user_id,
            'paraContent': para_content,
            'writeDate': write_date
        }
        #mongo_db.paragraph.insert_one(paragrpah)
        print(paragrpah)
    else:
        return jsonify({'msg': '저장실패!'})
    return jsonify({'msg': '저장성공!'})

@detail_blueprint.route("/delete_paragraph", methods=['POST'])
def delete_paragraph():
    if request.method == 'POST':
        para_num = request.form.get('paraNum')
       #mongo_db.paragraph.delete_one({'paraNum': para_num})
    else:
        return False
    return jsonify({'msg' : '삭제성공!'})

