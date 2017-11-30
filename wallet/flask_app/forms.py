from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[Length(min=16, max=16), DataRequired()])