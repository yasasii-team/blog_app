# coding: utf-8
from blog_app import app
from flask import Flask, render_template, jsonify, abort,request
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
        result = {'id': id}
        return jsonify(result), 201
    else:
        return abort(403)

# @app.route('/')
# def index():
#     return "Hello World"
