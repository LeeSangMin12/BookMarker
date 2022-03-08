from flask import Blueprint, render_template

detail_blueprint = Blueprint("detail", __name__, url_prefix="/detail")


@detail_blueprint.route("/detail")
def detail():
    return render_template("detail/detail.html", str="detail 나와요?")
