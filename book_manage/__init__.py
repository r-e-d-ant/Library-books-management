
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from enum import unique
from flask_login import LoginManager

app = Flask(__name__)
# set the required secret key
app.config['SECRET_KEY'] = 'af2bbabd5fe56ed015a8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookslibray.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from book_manage.forms import Upload, Borrow, LoginForm, RegistrationForm
from book_manage import routes

with app.app_context():
    db.create_all()
