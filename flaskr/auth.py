import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix = "/auth")

# ユーザー登録
@bp.route("/register", methods = ["GET", "POST"])
def register():
    # ユーザーがフォームを提出したときのメソッドはPOSTになる
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "ユーザーネームを入力してください."
        elif not password:
            error = "パスワードを入力してください."
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                # データベースを編集したため, それを反映させる.
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                # ユーザー登録が完了したらログインページにリダイレクトする
                # url_for()は引数の示すビューへのURLを生成. url変えたくなったときに便利.
                return redirect(url_for("auth.login"))
        
        # flash()はメッセージを保存しておける. テンプレートのHTML内でget_flashed_message()すると取り出せる.
        flash(error)

    return render_template("auth/register.html")

# ログイン
@bp.route("/login", methods = ("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "登録されていないユーザーネームが入力されています."
        elif not check_password_hash(user["password"], password)
            error = "パスワードが違います."
        
        if error is None:
            # sessionはflaskの組み込み辞書? サーバーとのやりとりにおいて, 改ざん防止のために存在するっぽい.
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        
        flash(error)
    return render_template("auth/login.html")

# どのURLにリクエストがなされても, load_logged_in_user()が実行される
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

# ログアウト
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    
    return wrapped_view