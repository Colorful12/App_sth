import os

from flask import Flask

def create_app(test_config=None):
    #アプリの作成＆構成
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "flaskr.sqlite"),
        ## app.instance_path Flaskがインスタンスフォルダとして選んだdirのパス
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    #インスタンスフォルダの作成
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #はろーわーるどするだけのページ
    @app.route("/hello")
    def hello():
        return "Hello, World!!"
    
    @app.route("/hello/cats")
    def nyallo():
        return "Nyallo, cats!!"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint = "index")

    # add_url_rule は, endpoint引数で指定した値とurl_forの引数が一致する場合に
    # URLを第一引数に変換する. ∴ url_for("index") = "/"
    

    return app
