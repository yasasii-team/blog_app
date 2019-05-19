import sqlite3

def test_dbmanage():
    conn=sqlite3.connect('test.db')
    c=conn.cursor()
    c.execute("select * from posts")
    posts = c.fetchall()
    c.close()
    conn.close()
    return posts
