# coding: utf-8
import os
from blog_app import app
import datetime
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
    user_id = 'test_user'

    #POST:登録処理
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title or not body:
            alert = 'タイトルと本文は必須入力です'
            return render_template('add.html', alert=alert, title=title, body=body)
        else:
            con = sqlite3.connect(app.config["DATABASE"])
            c = con.cursor()

            #DBへのinsert関数ができたらそちらを使う
            #sqlite3.OperationalError: table posts has 4 columns but 3 values were supplied
            #idはautoincrement？
            c.execute('INSERT INTO posts VALUES (?,?,?)',(user_id,title,body))
            con.commit()

            #DBからのselect関数ができたらそちらを使う
            result = con.execute('''select * from posts order by id desc''')

            #成功したら詳細画面へ？（とりあえず、一覧が載ってるindexへ）
            return render_template('index.html', result=result)

    #登録画面へ
    if request.method == 'GET':
        return render_template('add.html')

