from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import urandom
from flask_login import LoginManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = urandom(16).hex()
app.config["USE_SESSION_FOR_NEXT"] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

from market import routes

