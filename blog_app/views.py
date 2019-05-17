# coding: utf-8
from flask import Flask, render_template
from blog_app import app
from DBManager import *

#下記動作未確認です。5/19
@app.route('/')
def index():
    posts = DBManager.get_all_posts()
    return render_template('index.html',posts = posts)

#下記動作未確認です。5/19
@app.route('post_detail/<post_id>')
def post_detail(post_id):
    title = DBManager.find(post_id).title
    body = DBManager.find(post_id).body
    #titleとbodyを引き出したいと思っていますが、引き出し方調査不足で未実装です。
    return render_template('post_detail.html',title = title, body = body)

# @app.route('/')
# def index():
#     return "Hello World"
