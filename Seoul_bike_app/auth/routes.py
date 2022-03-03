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
login_bp = Blueprint('login', __name__, url_prefix='/login')
signup_bp = Blueprint('signup', __name__, url_prefix='/signup')
blog_bp = Blueprint('blog', __name__, url_prefix='/blog')


@auth_bp.route('/')
def index():
    return 'Hello World this is /auth/ section'


@main_bp.route('/')
def index():
    return 'Hello World this is /main/ section'


@login_bp.route('/')
def login():
    return 'Hello World this is login section'


@signup_bp.route('/')
def signup():
    return 'Hello World this is signup section'

@blog_bp.route('/')
def blog():
    return 'Hello World this is blog section'
