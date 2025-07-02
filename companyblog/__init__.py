# companyblog/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from dotenv import load_dotenv  # <-- Load .env file
# Load environment variables from .env
load_dotenv()



app = Flask(__name__)

# Secret key from environment variable
app.secret_key = os.getenv('SECRET_KEY')


######################################
######## DATABASE SETUP ##############
######################################
#! Database connection (For PostgreSQL)
# connection string: 'postgresql://postgres:your_password@localhost:5432/flask_app_login_db'
# PostgreSQL connection string from .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Optional config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# Initialize extensions
db = SQLAlchemy(app)
Migrate(app, db)
######################################
######################################
######################################


######################################
########## LOGIN CONFIGS #############
######################################
#! Create login_manager
login_manager = LoginManager()

# Pass in app to login_manager
login_manager.init_app(app) # --> Configures your app to allow login from users
login_manager.login_view = 'users.login'# --> tells users what view to go to after they login
######################################
######################################
######################################

# Import your models so alembic sees it when you flask-migrate
from companyblog import models # --> Must be placed here after Initialization




from companyblog.core.views import core
from companyblog.users.views import users
from companyblog.error_pages.handlers import error_pages
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)

