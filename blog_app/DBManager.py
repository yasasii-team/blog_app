from __future__ import with_statement
from blog_app import app
import sqlite3

class DBManager():
    def __init__(self):
        self.db = sqlite3.connect(app.config["DATABASE"])
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def init_db(self):
        with app.open_resource("schema.sql") as f:
            self.cursor.executescript(f.read().decode("utf-8"))
        self.db.commit()

    def get_all_posts(self):
        sql = "select * from posts order by created_at desc"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()

    def get_post(self, id: int):
        sql = "select * from posts where id=?;"
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchall()[0]

    def create_post(self, user_id: int, title: str, body: str):
        result = True
        try:
            sql = "insert into posts(user_id, title, body, created_at, updated_at) values(?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'));"
            self.db.execute(sql, [user_id, title, body])
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result

    def update_post(self, id: int ,title: str, body: str):
        result = True
        try:
            sql = "update posts set title = ?, body = ?, updated_at = datetime('now', 'localtime') where id = ?;"
            self.db.execute(sql, [title, body, id])
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result

    def delete_post(self, id: int):
        result = True
        try:
            sql = "delete from posts where id = ?;"
            self.db.execute(sql, (id,))
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result

    def get_user_by_id(self, id: int):
        sql = "select * from users where id=?;"
        self.cursor.execute(sql, (id,))
        users = self.cursor.fetchall()
        if users:
            return users[0]
        else:
            return None

    def update_user(self, id: int, email: str, password: str):
        result = True
        try:
            sql = "update users set email = ?, password = ?, updated_at = datetime('now', 'localtime') where id = ?;"
            self.db.execute(sql, [email, password, id])
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            result = False
        return result