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

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    #ログイン機能に合わせて要書き換え
    user_id = 1

    #ログインしているユーザーの情報を取得
    blog_db = DBManager()
    login_user = blog_db.get_user_by_id(user_id)
    if not login_user:
        session['alert'] = '不正なアクセスです'
        return redirect(url_for('index'))        

    #POST:ユーザー更新処理
    if request.method == 'POST':
        email = request.form['email']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']
        session['email'] = email

        if not email or not password_1 or not password_2:
            session['alert'] = 'e-mailとパスワードは必須入力です'
            return render_template('update_user.html') 
        elif password_1 != password_2:
            session['alert'] = 'パスワードが異なります'
            return render_template('update_user.html')             
        else:
            result = blog_db.update_user(user_id, email, password_1)
            blog_db.close()
            
            if result:
                return redirect(url_for('index'))           
            else:
                session['alert'] = 'ユーザー更新に失敗しました'
                return render_template('update_user.html') 

    #ユーザー更新画面へ
    else:
        session.pop('alert', None)
        session['email'] = login_user['email']
        return render_template('update_user.html')

# @app.route('/')
# def index():
#     return "Hello World"
