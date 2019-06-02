from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config.from_object("blog_app.config")
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = app.config['SECRET_KEY'] 

from blog_app import views