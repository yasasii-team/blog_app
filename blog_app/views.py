# coding: utf-8
from blog_app import app
from flask import render_template, jsonify, abort, request, url_for, redirect, session
from blog_app.DBManager import DBManager


@app.route('/')
def index():
    posts = DBManager().get_all_posts()
    return render_template('index.html',posts = posts)

@app.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = DBManager().get_post(post_id)
    return render_template('post_detail.html',post = post)

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

@app.route('/sign_up', methods=['GET', 'POST'])
def create_user():
    #POST:ユーザー登録処理
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        session['username'] = username
        session['email'] = email
        session['password'] = password

        if not username or not email or not password:
            session['alert'] = 'ユーザー名とe-mailとパスワードは必須入力です'
            return render_template('sign_up.html') 
        else:
            blog_db = DBManager()

            #ユーザーID重複チェック
            if blog_db.get_user(username):
                session['alert'] = 'ユーザー名は既に存在しています'
                blog_db.close()
                return render_template('sign_up.html') 
            result = blog_db.create_user(username, email, password)
            blog_db.close()
            
            if result:
                return redirect(url_for('index'))           
            else:
                session['alert'] = 'ユーザー登録に失敗しました'
                return render_template('sign_up.html') 

    #登録画面へ
    else:
        session.pop('alert', None)
        session.pop('username', None)
        session.pop('email', None)
        session.pop('password', None)
        return render_template('sign_up.html')

# @app.route('/')
# def index():
#     return "Hello World"
