# coding: utf-8
from flask import Flask, render_template
from blog_app import app
# from DBManager import *
from blog_app import test_dbmanage

#下記動作未確認です。5/19
@app.route('/')
def index():
    # 5/19仮にtest_dbmanage.pyからデータを取得しています。
    # posts = DBManager.get_all_posts()
    posts = test_dbmanage()
    return render_template('index.html',posts = posts)

@app.route('/post_detail/<post_id>')
def post_detail(post_id):
    # 5/19メソッド決まり次第DBManagerメソッドに修正します。
    # title = DBManager.find(post_id).title
    # body = DBManager.find(post_id).body

    # 5/19仮にtest_dbmanage.pyからデータを取得しています。
    posts = test_dbmanage()
    title = posts[int(post_id)][1]
    body = posts[int(post_id)][2]
    return_btn = '/'
    return render_template('post_detail.html',title = title, body = body, return_btn = return_btn)

# @app.route('/')
# def index():
#     return "Hello World"
