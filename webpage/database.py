#Used https://flask.palletsprojects.com/en/1.1.x/tutorial/database/, flask tutorial for making a database
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
#print("current_folder is " + current_folder + "\n") -> debug
DATABASE_PATH = os.path.join(current_folder, 'sqlite.db')

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            "sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e = None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("usertable.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)