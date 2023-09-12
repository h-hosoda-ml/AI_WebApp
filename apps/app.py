from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from pathlib import Path
from apps.config import config

# SQLAlchemyをインスタンス
db = SQLAlchemy()

# LoginManagerクラスをインスタンス化する
login_manager = LoginManager()

# 未ログインの時にリダイレクトするエンドポイントを指定
login_manager.login_view = "auth.login"

# ログインの後に表示するメッセージの指定
login_manager.login_message = ""


# create_app関数の作成
def create_app(config_key):
    # Flaskインスタンスの作成
    app = Flask(__name__)

    # config_keyにマッチする環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])

    # SQLAlchemyとappを連携する
    db.init_app(app)

    # Migrateとアプリを連携する
    Migrate(app, db)

    # login_managerをアプリケーションと連携
    login_manager.init_app(app)

    # user_managementアプリを登録
    from apps.user_management import views as usm_views

    app.register_blueprint(usm_views.user_management, url_prefix="/user_management")

    # authアプリを登録
    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    # classifyアプリを登録
    from apps.classify import views as cl_views

    app.register_blueprint(cl_views.classify, url_prefix="/classify")

    return app
