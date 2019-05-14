from __future__ import with_statement
from blog_app import app
import sqlite3

class DBManager():
    def __init__(self):
        self.db = sqlite3.connect(app.config["DATABASE"])
        self.cursor = self.db.cursor()

    def init_db(self):
        with app.open_resource("schema.sql") as f:
            self.cursor.executescript(f.read().decode("utf-8"))
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()

    def find(self, id: int):
        sql = "select * from posts where id=?;"
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchall()[0]

    def create(self, user_id: int, title: str, body: str):
        result = True
        try:
            sql = "insert into posts(user_id, title, body, created_at, updated_at) values(?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'));"
            self.db.execute(sql, [user_id, title, body])
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result