from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[Length(min=16, max=16), DataRequired()])

class MakeTransactionForm(FlaskForm):
    receiver = StringField('receiver', validators=[DataRequired()])
    amount = FloatField('amount', validators=[NumberRange(min=0), DataRequired()])

class CreateAddressForm(FlaskForm):
    password = PasswordField('password', validators=[Length(min=16, max=16), DataRequired()])
    label = StringField('label')