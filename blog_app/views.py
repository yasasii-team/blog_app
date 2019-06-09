# coding: utf-8
from blog_app import app
from flask import render_template, jsonify, abort, request, url_for, redirect, session
from blog_app.DBManager import DBManager
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

@app.route('/')
def index():
    posts = DBManager().get_all_posts()
    return render_template('index.html',posts = posts)

@app.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = DBManager().get_post(post_id)
    return render_template('post_detail.html',post = post)

@app.route('/signin', methods=['GET','POST'])
def signin():

    #user1のメールアドレスとパスワードをデータベースより取得
    sql = 'select email, password from users;'
    db = DBManager()
    db.cursor.execute(sql)
    signin_info = db.cursor.fetchall()
    email = signin_info[0][0]
    password = signin_info[0][1]
    db.close()

    session.pop('emailalert', None)
    session.pop('passwordalert', None)

    if request.method == 'POST':
        if request.form['email'] != email:
            session['emailalert'] = 'メールアドレスが間違っています'
        elif request.form['password'] != password:
            session['passwordalert'] = 'パスワードが間違っています'
        else:
            session['user_id'] = 1
            return redirect(url_for('index'))
    return render_template('signin.html')

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def create_page():

    #ログイン時にセッションに入れておく
    user_id = 1

    #POST:登録処理
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        session['title'] = title
        session['body'] = body

        if not title or not body:
            session['alert'] = 'タイトルと本文は必須入力です'
            return render_template('add.html')
        else:
            blog_db = DBManager()
            result = blog_db.create_post(user_id, title, body)
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

def check_and_get_post(id,blog_db):
    # 該当する投稿があるかのチェック
    if not id:
        # /update/にアクセスしたときにトップに返るようにするつもりだがうまく動いていないので要修正
        session['alert'] = "不正なアクセスです"
        blog_db.close()
        return redirect(url_for('index'))

    post = blog_db.get_post(id)

    if not post:
        # 該当する投稿がなかった時にトップに返るようにするつもりだがうまく動いていないので要修正
        session['alert'] = "該当する投稿がありません"
        blog_db.close()
        return redirect(url_for('index'))
    return post

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_page(post_id):
    #POST:更新処理
    if request.method == 'POST':
        post_id = request.form['post_id']
        title = request.form['title']
        body = request.form['body']

        session['post_id'] = post_id
        session['title'] = title
        session['body'] = body

        if not title or not body:
            session['alert'] = 'タイトルと本文は必須入力です'
            return render_template('update.html')
        else:
            blog_db = DBManager()
            post = check_and_get_post(post_id, blog_db)
            result = blog_db.update_post(post_id ,title, body)
            blog_db.close()

            if result:
                return redirect(url_for('post_detail', post_id=post_id))
            else:
                session['alert'] = 'データベース登録に失敗しました'
                return render_template('update.html')

    #GET：入力
    else:
        blog_db = DBManager()
        post = check_and_get_post(post_id, blog_db)
        session.pop('alert', None)
        session['post_id'] = post_id
        session['title'] = post['title']
        session['body'] = post['body']
        blog_db.close()
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
