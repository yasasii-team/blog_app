# coding: utf-8
import os
from blog_app import app
from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
#後で実装する用
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
#from wtforms.validators import Required

app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template("index.html")
    #return "Hello World"

@app.route('/add', methods=['GET', 'POST'])
def create_page():
    #ユーザー登録処理実装後に要修正(ログインチェック)
    user_id = 1

    #POST:登録処理
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        date_time = datetime.now()

        if not title or not body:
            alert = 'タイトルと本文は必須入力です'
            return render_template('add.html', alert=alert, title=title, body=body)
        else:
            con = sqlite3.connect(app.config["DATABASE"])
            c = con.cursor()

            #DBへのinsert関数ができたらそちらを使う
            c.execute('INSERT INTO posts(user_id, title, body, created_at, updated_at) \
                values(?, ?, ?, ?, ?)',\
                (user_id, title, body, date_time, date_time))
            con.commit()

            #DBからのselect関数ができたらそちらを使う
            result = con.execute('''select * from posts order by updated_at desc''')

            #成功したら詳細画面へ？（とりあえず、一覧が載ってるindexへ）
            return render_template('index.html', result=result)

    #登録画面へ
    else:
        return render_template('add.html')

