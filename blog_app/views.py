# coding: utf-8
import os
from blog_app import app
from datetime import datetime
import sqlite3
from blog_app.DBManager import DBManager
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFProtect
#後で実装する用
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
#from wtforms.validators import Required

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
    try:
        data= {'title': '', 'body': ''}

        #ユーザー登録処理実装後に要修正(ログインチェック)
        #セッションで管理するから辞書に入れる必要はないかも
        data['user_id'] = 1

        #POST:登録処理
        if request.method == 'POST':
            data['title'] = request.form['title']
            data['body'] = request.form['body']

            if not data['title'] or not data['body']:
                alert = 'タイトルと本文は必須入力です'
                return render_template('add.html', alert=alert, data=data)
            else:
                blogDB = DBManager()
                result = blogDB.create_post(data['user_id'], data['title'], data['body'])
                blogDB.close()

                if result:
                    # 成功したら詳細画面へ？（とりあえず、一覧が載ってるindexへ）
                    # post_id不明
                    # return redirect(url_for('post_detail'), post_id=post_id)
                    return redirect(url_for('index'))           
                else:
                    alert = 'データベース登録に失敗しました'
                    return render_template('add.html', alert=alert, data=data)

        #登録画面へ
        else:
            return render_template('add.html', data=data)
            
    except KeyError as e:
        print(e)
        return redirect(url_for('index'))

def check_and_get_post(id):
    # 該当する投稿があるかのチェック
    if not id:
        alert = "不正なアクセスです" 
        # render_templateでalert送る？
        return redirect(url_for('index'))

    blogDB = DBManager()
    post = blogDB.get_post(id)

    if len(post) < 1:
        alert = "該当する投稿がありません" 
        return redirect(url_for('index'))

    return post


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_page(post_id):
    try:
        data= {'title': '', 'body': ''}

        #ユーザー登録処理実装後に要修正(ログインチェック)
        #セッションで管理するから辞書に入れる必要はないかも
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
                blogDB = DBManager()
                result = blogDB.update_post(data['id'] ,data['title'], data['body'])
                blogDB.close()

                if result:
                    # 成功したら詳細画面へ？（とりあえず、一覧が載ってるindexへ）
                    # return redirect(url_for('post_detail'), post_id=data['id'])
                    return redirect(url_for('index'))           
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

    except KeyError as e:
        print(e)
        return redirect(url_for('index'))
