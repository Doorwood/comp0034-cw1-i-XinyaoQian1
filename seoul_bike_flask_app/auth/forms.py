"""
# @File    :    forms.py
# @Time    :    02/02/2022 13:52
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description:   The forms used in flask app.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, EqualTo

from seoul_bike_flask_app.models import User


class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[
        DataRequired(message='First name required')])
    last_name = StringField(label='Last name', validators=[
        DataRequired(message='Last name required')])
    email = EmailField(label='Email address', validators=[
        DataRequired(message='Email address required')
    ])
    password = PasswordField(label='Password', validators=[
        DataRequired(message='Password required')])
    password_repeat = PasswordField(label='Confirm Password',
                                    validators=[DataRequired(),
                                                EqualTo('password',
                                                        message='Passwords must match!')])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError(
                'An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password.')
