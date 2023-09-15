from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, login_user
from apps.app import db
from apps.user_management.models import User
from apps.user_management.forms import UserForm, AdminLoginForm

from .utils import admin_required

# user_managementアプリの作成
user_management = Blueprint(
    "user_management",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# ユーザーの一覧
@user_management.route("/")
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template("user_management/index.html", users=users)


# ユーザーの新規作成
@user_management.route("/new", methods=["GET", "POST"])
@login_required
@admin_required
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


# ユーザー編集画面
@user_management.route("/edit/<user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    form = UserForm()

    user = User.query.filter_by(id=user_id).first()

    # formからサブミットされた場合はユーザーを更新して一覧画面へリダイレクト
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_management.index"))

    return render_template("user_management/edit.html", user=user, form=form)


# ユーザーの削除処理を行うエンドポイント(Postのみ)
@user_management.route("/edit/<user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("user_management.index"))
