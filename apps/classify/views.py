from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

import numpy as np
import base64
import cv2

import datetime
import re

from .mnist.predict import predict

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
        prediction = get_digits_predict(request)
        return jsonify({"prediction": prediction})

    # GET処理だった場合
    else:
        return render_template("classify/digitsdraw.html")


# 予測結果を返す関数
def get_digits_predict(req: request):
    # DataURLからデータ部分だけを抽出
    img_str = re.search(r"base64,(.*)", req.form["img"]).group(1)

    # base64モジュールを利用してndarray配列へ変換
    np_arr = np.fromstring(base64.b64decode(img_str), np.uint8)

    # opencv画像として読み込む
    img_src = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 色の反転
    img_negaposi = 255 - img_src

    # グレースケールに変換
    img_gray = cv2.cvtColor(img_negaposi, cv2.COLOR_BGR2GRAY)

    # (28, 28)にリサイズ
    img_resize = cv2.resize(img_gray, (28, 28))

    pred: int = predict(img_resize)

    return pred
