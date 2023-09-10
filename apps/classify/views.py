from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

# classifyアプリ
classify = Blueprint(
    "classify", __name__, template_folder="templates", static_folder="static"
)


# indexエンドポイント
@classify.route("/")
def index():
    return render_template("classify/index.html")


# digitsdrawエンドポイントの作成
@classify.route("/digitsdraw", methods=["GET", "POST"])
@login_required
def digitsdraw():
    # POSTされた場合
    if request.method == "POST":
        # TODO: cnnモデルによる予測を行い結果を返す処理の作成
        pass

    # GET処理だった場合
    else:
        return render_template("classify/digitsdraw.html")
