import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g:
        g.db = splite3.connect(
            current_app.config["DATABASE"],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        get_db.row_factory = splite3.Row

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
