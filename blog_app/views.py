# coding: utf-8
import os
from blog_app import app
from flask import Flask, render_template, jsonify, abort, request, url_for, redirect, session
from blog_app.DBManager import DBManager 
from flask_wtf.csrf import CSRFProtect

app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = app.config['SECRET_KEY'] 
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

    #ログイン時にセッションに入れておく
    user_id = 1

    #POST:登録処理
    if request.method == 'POST':
        session['title'] = request.form['title']
        session['body'] = request.form['body']

        if not session['title'] or not session['body']:
            session['alert'] = 'タイトルと本文は必須入力です'
            return render_template('add.html') 
        else:
            blog_db = DBManager()
            result = blog_db.create_post(user_id, session['title'], session['body'] )
            blog_db.close()

            if result:
                return redirect(url_for('index'))           
            else:
                session['alert'] = 'データベース登録に失敗しました'
                return render_template('add.html') 

    #登録画面へ
    else:
        session.pop('alert', None)
        session.pop('title', None)
        session.pop('body', None)
        return render_template('add.html') 


def check_and_get_post(id):
    # 該当する投稿があるかのチェック
    if not id:
        # /update/にアクセスしたときにトップに返るようにするつもりだがうまく動いていないので要修正
        session['alert'] = "不正なアクセスです" 
        return redirect(url_for('index'))

    blog_DB = DBManager()
    post = blog_DB.get_post(id)

    if not post:
        # 該当する投稿がなかった時にトップに返るようにするつもりだがうまく動いていないので要修正
        session['alert'] = "該当する投稿がありません" 
        return redirect(url_for('index'))
    return post

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_page(post_id):
    #POST:更新処理
    if request.method == 'POST':

        post = check_and_get_post(request.form['post_id'])
        session['post_id'] = request.form['post_id']
        session['title'] = request.form['title']
        session['body'] = request.form['body']

        if not session['title'] or not session['body']:
            session['alert'] = 'タイトルと本文は必須入力です'
            return render_template('update.html') 

        else:
            blog_db = DBManager()
            result = blog_db.update_post(session['post_id'] ,session['title'], session['body'])
            blog_db.close()

            if result:
                return redirect(url_for('post_detail', post_id=session['post_id'] ))   
            else:
                session['alert'] = 'データベース登録に失敗しました'
                return render_template('update.html')

    #GET：入力
    else:
        post = check_and_get_post(post_id)
        session.pop('alert', None)
        session['post_id'] = post_id
        session['title'] = post['title']
        session['body'] = post['body']
        return render_template('update.html')
@app.route('/delete', methods=['POST'])
def delete():
    id = request.json['id']
    db_manager = DBManager()
    if db_manager.delete_post(id):
        db_manager.close()
        result = {'id': id}
        return jsonify(result), 201
    else:
        db_manager.close()
        return abort(403)

# @app.route('/')
# def index():
#     return "Hello World"
