from flask import Blueprint, render_template
from flask_login import login_required,login_url,login_user,current_user,logout_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    return render_template('index.html', title="Home")