#Used https://realpython.com/flask-google-login/ as a source
from flask_login import UserMixin
from database import get_db
import os.path
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sqlite.db")
with sqlite3.connect(db_path) as db:

    class User(UserMixin):
        def __init__(self, id_, profile_pic, name, email):
            self.id = id_
            self.profile_pic = profile_pic
            self.name = name
            self.email = email

        @staticmethod
        def get(user_id):
            db = get_db()
            user = db.execute(
                "SELECT * FROM user WHERE id = ?", (user_id,)
            ).fetchone()
            if not user:
                return None

            user = User(
                id_=user[0], profile_pic=user[1], name=user[2], email=user[3]
            )
            return user      

        @staticmethod
        def create(id_, profile_pic, name, email):
            db = get_db()
            db.execute(
                "INSERT INTO user (id, profile_pic, name, email) "
                "VALUES (?, ?, ?, ?)",
                (id_, profile_pic, name, email),
            )
            db.commit()  