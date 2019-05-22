# coding: utf-8
from blog_app import app
from flask import Flask, render_template
from blog_app.DBManager import DBManager


@app.route('/')
def index():
    posts = DBManager().get_all_posts()
    return render_template('index.html',posts = posts)

@app.route('/post_detail/<post_id>')
def post_detail(post_id):
    post = DBManager().get_post(post_id)
    return render_template('/post_detail',post = post)


# @app.route('/')
# def index():
#     return "Hello World"
