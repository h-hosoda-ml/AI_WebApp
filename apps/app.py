from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from pathlib import Path
from apps.config import config

# SQLAlchemyをインスタンス
db = SQLAlchemy()


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

    # user_managementアプリを登録
    from apps.user_management import views as user_management_views

    app.register_blueprint(
        user_management_views.user_management, url_prefix="/user_management"
    )

    return app
