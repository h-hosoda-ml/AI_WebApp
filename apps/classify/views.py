from flask import Blueprint, render_template


# classifyアプリ
classify = Blueprint(
    "classify", __name__, template_folder="templates", static_folder="static"
)


# indexエンドポイント
@classify.route("/")
def index():
    return render_template("classify/index.html")
