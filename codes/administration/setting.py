from flask import Flask, render_template,redirect,session, url_for, flash, blueprints, Blueprint, request
from functools import wraps
from codes.db.db import create_connections
from sqlalchemy import create_engine, text
from werkzeug.security import check_password_hash
# from codes.routes.admin import admin
# from codes.routes.superadmin import superadmin
# from codes.routes.users import user
# from codes.routes.manager import manager
import os
import sys
from werkzeug.utils import secure_filename
from codes.api import *
# from codes.queries import *

engine = create_connections()

setting = Blueprint('setting', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def loginRequire(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session and 'role' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@setting.route('/security-settings', methods=['GET', 'POST'])
@loginRequire
def security_settings():
    employee_id = session.get('employee_id')
    user_details = get_user_details(session['username'])

    return render_template('user/settings/general_settings/security-settings.html', 
                           user_details=user_details)
    
    
