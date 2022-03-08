from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import certifi
detail_blueprint = Blueprint("detail", __name__, url_prefix="/detail")

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.lafvq.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
mongo_db = client.bookmaker


@detail_blueprint.route("/detail/<keyword>")
def detail(keyword):
    book = mongo_db.books.find_one({'bookNum': keyword})
    paragraph = list(mongo_db.paragraph.find({'bookNum': keyword},{}))
    return render_template("detail/detail.html", book=book, paragraph=paragraph)


# 코멘트 작성
@detail_blueprint.route("/write_paragraph", methods=["POST"])
def write_paragraph():
    if request.method == 'POST':
        book_num = request.form.get('bookNum')
        user_id = request.form.get('userId')
        para_content = request.form.get('paraContent')
        write_date = request.form.get('writeDate')
        max_para_num = mongo_db.paragraph.find_one(sort=[("paraNum", -1)])
        new_para_num = int(max_para_num['paraNum'])+1
        paragrpah = {
            'bookNum': book_num,
            'paraNum': new_para_num,
            'userId': user_id,
            'paraContent': para_content,
            'writeDate': write_date
        }
        mongo_db.paragraph.insert_one(paragrpah)
    else:
        return jsonify({'msg': '저장실패!'})
    return jsonify({'msg': '저장성공!'})


@detail_blueprint.route("/delete_paragraph", methods=['POST'])
def delete_paragraph():
    if request.method == 'POST':
        para_num = request.form.get('paraNum')
        print(para_num)
        mongo_db.paragraph.delete_one({'paraNum': int(para_num)})
    else:
        return False
    return jsonify({'msg' : '삭제성공!'})




