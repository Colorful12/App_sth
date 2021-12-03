import os

from flask import Flask

def create_app(test_config=None):
    #アプリの作成＆構成
    app = Flask(__name__, instance_relative_config=True)
    app.config.form_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "flaskr.sqlite"),
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

    return app
