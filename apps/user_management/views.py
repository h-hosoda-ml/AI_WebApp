from flask import Blueprint, render_template

# user_managementアプリの作成
user_management = Blueprint(
    "user_management",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# indexエンドポイントを作成してindex.htmlを返す
@user_management.route("/")
def index():
    return render_template("user_management/index.html")
