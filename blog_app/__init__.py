from flask import Flask

app = Flask(__name__)
# app.config.from_object("blog_app.config")

from blog_app import views
