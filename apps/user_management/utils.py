from flask import flash, redirect, url_for
from flask_login import current_user, login_required
from functools import wraps


# アドミンユーザーの権限が必要なページに付与するデコレータ
def admin_required(func):
    @wraps(func)
    def decoreted_view(*args, **kwargs):
        if not current_user.is_admin:
            flash("管理者ページにはアクセスできません。", "danger")
            return redirect(url_for("classify.index"))
        return func(*args, **kwargs)

    return decoreted_view
