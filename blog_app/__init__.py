from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object("blog_app.config")
csrf = CSRFProtect(app)

from blog_app import views