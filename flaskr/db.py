import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g:
        # "DATABASE"で示されたファイルとのコネクションをつくる. 
        # そのファイルはこの段階で存在する必要はなく, あとでinitializeするまでその状態は続く.
        g.db = splite3.connect(
            # currnet_appはdb.pyをインポートしたプログラムを示すってことか？
            current_app.config["DATABASE"],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        # 列名での参照ができるようにコネクションを確立.
        get_db.row_factory = splite3.Row

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
     with current_app.open_resource("schema.sql") as f:
         db.executescript(f.read().decode("utf8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    """存在するデータを消して, 新しい表を作成する"""
    init_db()
    click.echo("Initialized the database.")
