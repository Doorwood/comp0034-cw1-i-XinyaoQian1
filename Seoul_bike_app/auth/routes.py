"""
# @File    :    routes.py
# @Time    :    23/02/2022 19:13
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
# app.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

main_bp = Blueprint('main', __name__, url_prefix='/main')


@auth_bp.route('/')
def index():
    return 'Hello World this is /auth/ section'


@main_bp.route('/')
def index():
    return 'Hello World this is /main/ section'
