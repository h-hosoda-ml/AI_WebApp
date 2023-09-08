from flask import Blueprint, render_template, flash, url_for, redirect, request
from apps.app import db
from apps.auth.forms import SignUpForm
from apps.user_management.models import User
from flask_login import login_user

# blueprintを使ってauthを生成する
auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


# indexエンドポイントを作成
@auth.route("/")
def index():
    return render_template("auth/index.html")


# signupエンドポイントを作成
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpFormをインスタンス化
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # メールの重複を確認
        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))

        # ユーザー情報を登録する
        db.session.add(user)
        db.session.commit()

        # ユーザー情報をセッションに格納する
        login_user(user)
        # GETパラメータにnextキーが存在して、値がない場合はユーザーの一覧ページへ
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("user_management.users")
        return redirect(next_)

    return render_template("auth/signup.html", form=form)
