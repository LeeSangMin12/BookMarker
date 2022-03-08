from flask import Blueprint, render_template

login_blueprint = Blueprint("login", __name__, url_prefix="/login")


@login_blueprint.route("/login")
def login():
    return render_template("login/login.html", str="로그인창 나와요?")


