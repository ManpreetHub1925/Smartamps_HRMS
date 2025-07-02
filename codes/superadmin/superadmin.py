from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from contextlib import closing
from datetime import datetime
from urllib.parse import urlencode
import json
from sqlalchemy import text
from codes.db.db import create_connections
from flask import current_app
import re
from functools import wraps
from codes.api import *

superadmin = Blueprint('superadmin', __name__)

def loginRequire(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session and 'role' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@superadmin.route('/dashboard-superadmin', methods=['GET'])
@loginRequire
def dashboard():
    emp_code = session.get('employee_id')
    
    user_details = get_user_details(session['username'])
 
        
    if not user_details:
        # Optionally redirect to error page or show message
        return "User details not found", 404

    return render_template('user/dashboards/superadmin_dashboard.html',
                        user_details=user_details)



