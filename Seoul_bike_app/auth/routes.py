"""
# @File    :    routes.py
# @Time    :    23/02/2022 19:13
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
# app.py

from flask import Blueprint, render_template, flash, redirect, url_for, request
from .forms import SignupForm

auth_bp = Blueprint('auth', __name__)
# main_bp = Blueprint('main', __name__, url_prefix='/main')



@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        return f"Hello, {name}. You are signed up."
    return render_template('signup.html',title='Sign Up', form=form)


