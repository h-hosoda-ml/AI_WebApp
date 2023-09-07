from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.user_management.models import User
from apps.user_management.forms import UserForm

# user_managementアプリの作成
user_management = Blueprint(
    "user_management",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# ユーザーの一覧
@user_management.route("/")
def users():
    users = User.query.all()
    return render_template("user_management/index.html", users=users)


# ユーザーの新規作成
@user_management.route("/new", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    # フォームの値をバリデート
    if form.validate_on_submit():
        # ユーザーの作成
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # ユーザーを追加してコミットする
        db.session.add(user)
        db.session.commit()
        # ユーザーの一覧画面へリダイレクト
        return redirect(url_for("user_management.index"))
    return render_template("user_management/create.html", form=form)
