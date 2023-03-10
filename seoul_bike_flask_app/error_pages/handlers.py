"""
# @File    :    handlers.py
# @Time    :    02/04/2022 13:52
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description:   The error handlers.
"""
from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)


@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404


@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html'), 403
