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

    def find_user_by_mail(self, email: str):
        sql = "select * from users where email=?;"
        self.cursor.execute(sql, (email,))
        users = self.cursor.fetchall()
        if users:
            return users[0]
        else:
            return None

    def find_user_by_id(self, id: int):
        sql = "select * from users where id=?;"
        self.cursor.execute(sql, (id,))
        users = self.cursor.fetchall()
        if users:
            return users[0]
        else:
            return None

    def find_user(self, email: str, password: str):
        sql = "select * from users where email=? and password=?;"
        self.cursor.execute(sql, (email, password,))
        return self.cursor.fetchone()

    def create_user(self, name: str, email: str, password: str):
        result = True
        try:
            sql = "insert into users(name, email, password, created_at, updated_at) values (?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'));"
            # ここでパスワードの暗号化処理を入れる
            self.db.execute(sql, (name, email, password,))
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result

    def update_user(self, user_id: int, name: str, email: str):
        result = True
        try:
            sql = "update users set name = ?, email = ?, updated_at = datetime('now', 'localtime') where id = ?;"
            self.db.execute(sql, (name, email, user_id, ))
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result
    
    def change_password(self, user_id: int, password: str):
        result = True
        try:
            sql = "update users set password = ?, updated_at = datetime('now', 'localtime') where id = ?;"
            # ここに暗号化処理を追加
            self.db.execute(sql, (password, user_id,))
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result

    def delete_user(self, user_id: int):
        result = True
        try:
            sql = "delete from users where id=?"
            self.db.execute(sql, (user_id,))
            self.db.commit()
        except:
            self.db.rollback()
            result = False
        return result