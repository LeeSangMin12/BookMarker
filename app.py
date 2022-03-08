from flask import Flask, render_template

import detail
import login

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


@app.route("/upload")
def upload():
    return render_template("upload.html", urlChk="False")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
