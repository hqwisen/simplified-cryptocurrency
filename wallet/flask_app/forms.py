from flask_wtf import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    password = PasswordField('password', validators=[Length(min=16, max=16), DataRequired()])