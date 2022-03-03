"""
# @File    :    forms.py
# @Time    :    03/03/2022 16:59
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField,SubmitField
from wtforms.validators import DataRequired, EqualTo

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError

class SignupForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')

