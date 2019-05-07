# coding: utf-8
from blog_app import app


@app.route('/')
def index():
    return "Hello World"
