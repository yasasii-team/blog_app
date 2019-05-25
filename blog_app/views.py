# coding: utf-8
import os
from blog_app import app
from blog_app.DBManager import DBManager
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFProtect

app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)

@app.route('/')
def index():
    posts = DBManager().get_all_posts()
    return render_template('index.html',posts = posts)

@app.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = DBManager().get_post(post_id)
    return render_template('post_detail.html',post = post)

@app.route('/add', methods=['GET', 'POST'])
def create_page():
    data= {'title': '', 'body': ''}

    #ユーザー登録処理実装後に要修正(ログインチェック)
    data['user_id'] = 1

    #POST:登録処理
    if request.method == 'POST':
        data['title'] = request.form['title']
        data['body'] = request.form['body']

        if not data['title'] or not data['body']:
            alert = 'タイトルと本文は必須入力です'
            return render_template('add.html', alert=alert, data=data)
        else:
            blog_db = DBManager()
            result = blog_db.create_post(data['user_id'], data['title'], data['body'])
            blog_db.close()

            if result:
                return redirect(url_for('index'))           
            else:
                alert = 'データベース登録に失敗しました'
                return render_template('add.html', alert=alert, data=data)

    #登録画面へ
    else:
        return render_template('add.html', data=data)


def check_and_get_post(id):
    # 該当する投稿があるかのチェック
    if not id:
        alert = "不正なアクセスです" 
        # alertはセッションで送るように要修正
        return redirect(url_for('index'))

    blog_DB = DBManager()
    post = blog_DB.get_post(id)

    if len(post) < 1:
        alert = "該当する投稿がありません" 
        return redirect(url_for('index'))

    return post

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_page(post_id):
    data= {'title': '', 'body': ''}

    #ユーザー登録処理実装後に要修正(ログインチェック)
    data['user_id'] = 1

    #POST:更新処理
    if request.method == 'POST':

        post = check_and_get_post(request.form['id'])

        data['id'] = request.form['id']
        data['title'] = request.form['title']
        data['body'] = request.form['body']

        if not data['title'] or not data['body']:
            alert = 'タイトルと本文は必須入力です'
            return render_template('update.html', alert=alert, data=data, post_id=post_id)

        else:
            blog_db = DBManager()
            result = blog_db.update_post(data['id'] ,data['title'], data['body'])
            blog_db.close()

            if result:
                return redirect(url_for('post_detail', post_id=data['id']))   
            else:
                alert = 'データベース登録に失敗しました'
                return render_template('update.html', alert=alert, data=data, post_id=post_id)

    #GET：入力
    else:
        post = check_and_get_post(post_id)
        data['id'] = post_id
        data['title'] = post['title']
        data['body'] = post['body']
        return render_template('update.html', data=data, post_id=post_id)

# @app.route('/')
# def index():
#     return "Hello World"
