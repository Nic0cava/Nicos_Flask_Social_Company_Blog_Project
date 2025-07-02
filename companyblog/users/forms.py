# companyblog/users/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
# allows user to update/upload a png file for their profile picture
from flask_wtf.file import FileField,FileAllowed
# related to users
from flask_login import current_user
from companyblog.models import User
