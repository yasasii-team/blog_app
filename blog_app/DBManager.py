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