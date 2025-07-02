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
from datetime import timedelta
from functools import wraps
import random
from codes.api import *
    
user = Blueprint('user', __name__)

engine = create_connections()


def loginRequire(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session and 'role' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user.route('/dashboard-users', methods=['GET'])
@loginRequire
def dashboard():
    
    employee_id = session['username']
    
    user_details=get_user_details(session['username'])
    
    return render_template('user/dashboards/admin_dashboard.html', user_details=user_details)

# @user.route('/', methods=['GET'])
# def index():
#     """Render Website"""
#     # return render_template('user/login_and_auth/L1_login.html')
#     return render_template('user/pages/error_500.html')
    


# def login_required_l1(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get('company_id'):
#             flash('Please login first', 'warning')
#             return redirect(url_for('user.login'))
#         return f(*args, **kwargs)
#     return decorated_function


# def login_required_l2(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get('username'):
#             flash('Please login first', 'warning')
#             return redirect(url_for('user.user_login'), company_id=session.get('company_id'))
#         return f(*args, **kwargs)
#     return decorated_function

   

# @user.route('/login', methods=['GET'])
# def login():
#     """Render company selection page with active companies"""
#     try:
#         with engine.connect() as conn:
#             companies = conn.execute(
#                 text("SELECT company_id, company_name FROM companies_details WHERE status = 'active'")
#             ).fetchall()
#         return render_template('user/L1_login.html', companies=companies)
#     except Exception as e:
#         current_app.logger.error(f"Error fetching companies: {str(e)}", exc_info=True)
#         flash('Unable to load company list. Please try again.', 'danger')
#         return render_template('user/login_and_auth/L1_login.html', companies=[])


# @user.route('/login_L1_auth', methods=['POST'])
# def login_L1_auth():
#     """Validate and store company selection"""
#     company_id = request.form.get('company_id')
    
#     try:
#         with engine.connect() as conn:
#             company = conn.execute(
#                 text("""
#                     SELECT company_id FROM companies_details 
#                     WHERE status = 'active' AND company_id = :company_id
#                 """),
#                 {'company_id': company_id}
#             ).fetchone()

#         if not company:
#             flash('Invalid company or company not active', 'danger')
#             return redirect(url_for('user.index'))

#         session.clear()
#         session['company_id'] = company_id
#         return redirect(url_for('user.login_user'))

#     except Exception as e:
#         current_app.logger.error(f"Company validation error: {str(e)}", exc_info=True)
#         flash('Error validating company. Please try again.', 'danger')
#         return redirect(url_for('user.index'))


# @user.route('/login_user', methods=['GET', 'POST'])
# @login_required_l1
# def login_user():
#     """Handle user authentication (L1)"""
#     company_id = session.get('company_id')

#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password') 
#         remember = request.form.get('remember_me') == 'on'

#         try:
#             with engine.connect() as conn:
#                 user = conn.execute(
#                     text("""
#                         SELECT company_id, username, password , emp_email_id
#                         FROM users 
#                         WHERE company_id = :company_id 
#                         AND (username = :username
#                             OR emp_email_id = :username
#                             OR emp_code = :username) and password = :password
#                         LIMIT 1
#                     """),
#                     {'company_id': company_id, 'username': username, 'password': password}
#                 ).fetchone()

#                 if not user:
#                     flash('Invalid credentials', 'danger')
#                     return render_template('user/login_and_auth/login.html', company_id=company_id)
                

#                 # Store masked email in session
#                 emp_email = user.emp_email_id
#                 masked_email = emp_email[0:3] + '****' + emp_email.split('@')[1] if '@' in emp_email else '****'
#                 session['masked_email'] = masked_email
                
#                 otp = f"{random.randint(1000, 9999):04d}"
#                 session['L2_auth_code'] = otp
#                 session['username'] = username
#                 session.permanent = remember  # For remember me functionality

#                 flash("OTP sent to your registered email.", 'success')

#                 # In production: Send via email or SMS
#                 print(f"OTP for {username}: {otp}")
#                 return redirect(url_for('user.L2_auth'))

#         except Exception as e:
#             current_app.logger.error(f"Login error: {str(e)}", exc_info=True)
#             flash('An error occurred during login. Please try again.', 'danger')
#             return render_template('user/login_and_auth/login.html', company_id=company_id)

#     return render_template('user/login_and_auth/login.html', company_id=company_id)


# @user.route('/L2_auth', methods=['GET', 'POST'])
# @login_required_l1
# def L2_auth():
#     """Handle second factor authentication"""
#     if 'L2_auth_code' not in session:
#         flash('Session expired. Please login again.', 'danger')
#         return redirect(url_for('user.index'))

#     if request.method == 'POST':
#         digit1 = request.form.get('digit-1', '')
#         digit2 = request.form.get('digit-2', '')
#         digit3 = request.form.get('digit-3', '')
#         digit4 = request.form.get('digit-4', '')
#         input_code = f"{digit1}{digit2}{digit3}{digit4}"
        
#         if len(input_code) != 4:
#             flash('Please enter the complete 4-digit code', 'warning')
#         elif input_code == session['L2_auth_code']:
#             session['authenticated'] = True
#             session.pop('L2_auth_code', None)
#             flash('Authentication successful', 'success')
#             return redirect(url_for('user.dashboard'))
#         else:
#             flash('Invalid authentication code', 'danger')
    
#     return render_template('user/login_and_auth/2fa_auth.html')


# @user.route('/resend_otp')
# @login_required_l1
# @login_required_l2
# def resend_otp():
#     # Generate new OTP
#     session['L2_auth_code'] = f"{random.randint(1000, 9999):04d}"
    
#     # In production: Send via email/SMS
#     print(f"New OTP for {session['username']}: {session['L2_auth_code']}")
    
#     return {'status': 'success', 'message': 'New OTP has been sent'}, 200



# def mask_email(email):
#     local, domain = email.split('@')
#     return local[0] + "****" + local[-1] + "@" + domain


# @user.route('/forgot_password', methods=['GET', 'POST'])
# @login_required_l1
# def forgot_password():
#     company_id = session.get('company_id')

#     if request.method == 'GET':
#         return render_template('user/forgot_password.html', step='email')

#     if request.method == 'POST':
#         email_id = request.form.get('email_id')
#         username = request.form.get('username')

#         try:
#             with engine.connect() as conn:
#                 user = conn.execute(
#                     text("""
#                         SELECT company_id, username, emp_email_id
#                         FROM users 
#                         WHERE company_id = :company_id 
#                           AND (username = :username
#                                OR emp_email_id = :username
#                                OR emp_code = :username)
#                           AND emp_email_id = :email_id
#                         LIMIT 1
#                     """),
#                     {
#                         'company_id': company_id,
#                         'username': username,
#                         'email_id': email_id
#                     }
#                 ).fetchone()
#                 print(user)

#                 if not user:
#                     flash('Invalid credentials', 'danger')
#                     return render_template('user/login_and_auth/forgot_password.html', company_id=company_id, step='email')

#             otp = f"{random.randint(1000, 9999):04d}"
#             session['L2_auth_code'] = otp
#             session['username'] = username
#             session['masked_email'] = mask_email(email_id)
#             flash("OTP sent to your registered email.", "info")
#             print(f"OTP for {username}: {otp}")
#             return render_template("user/login_and_auth/forgot_password.html", step='otp')

#         except Exception as e:
#             print(f"Error during user lookup: {e}")
#             flash("User not found or internal error occurred.", "danger")
#             return render_template("user/login_and_auth/forgot_password.html", step='email')
#     else:
#         flash("Invalid request method.", "danger")

#     return render_template("user/login_and_auth/forgot_password.html", step='email')


# @user.route('/verify_otp', methods=['POST'])
# @login_required_l1
# def otp_verify():
#     entered_otp = ''.join([
#         request.form.get('digit-1', ''),
#         request.form.get('digit-2', ''),
#         request.form.get('digit-3', ''),
#         request.form.get('digit-4', '')
#     ])
#     original_otp = session.get('L2_auth_code')

#     if entered_otp == original_otp:
#         flash("OTP verified. Proceed to reset password.", "success")
#         return render_template("user/login_and_auth/forgot_password.html", step='reset')
#     else:
#         flash("Invalid OTP. Please try again.", "danger")
#         return render_template("user/login_and_auth/forgot_password.html", step='otp')

    
# @user.route('/reset_password', methods=['GET', 'POST'])
# @login_required_l1
# def reset_password():
#     if request.method == 'POST':
#         company_id = session.get('company_id')
#         username = session.get('username')
#         new_pass = request.form.get('new_pass')
#         confirm_pass = request.form.get('confirm_pass')

#         if new_pass != confirm_pass:
#             flash("Passwords do not match.", "danger")
#             return render_template("user/login_and_auth/forgot_password.html", step='reset')

#         try:
#             with engine.begin() as conn:
#                 conn.execute(
#                     text("""
#                         UPDATE users
#                         SET password = :new_pass
#                         WHERE company_id = :company_id AND username = :username
#                     """),
#                     {'company_id': company_id, 'username': username, 'new_pass': new_pass}
#                 )
#             flash("Password reset successful. Please login.", "success")
#             return redirect(url_for('user.login_user'))

#         except Exception as e:
#             print(f"Error during password reset: {e}")  # Optional: log the error
#             flash("Error during reset. Try again.", "danger")
#             return render_template("user/login_and_auth/forgot_password.html", step='reset')

#     return render_template("user/login_and_auth/forgot_password.html", step='reset')


# @user.route('/logout')
# @login_required_l1
# @login_required_l2
# def logout():
#     session.clear() 
#     flash('You have been logged out successfully.', 'success')
#     return redirect(url_for('user.login'))


# @user.route('/profile')
# def profile():
#     username = session.get('username')
#     company_id = session.get('company_id')

#     try:
#         with engine.connect() as conn:
#             user = conn.execute(text("""
#             SELECT * FROM users 
#             WHERE company_id = :company_id 
#             AND (username = :username
#                 OR emp_email_id = :username
#                 OR emp_code = :username)
#         """), {'company_id': company_id, 'username': username}).fetchone()

#         user_data = {
#             'emp_code': user.emp_code,
#             'f_name': user.f_name,
#             'l_name': user.l_name,
#             'department': user.department,
#             'designation': user.designation

#         }
#         session['user_data'] = user_data

#     except:
#         pass

#     return render_template('user/login_and_auth/profile.html')


# @user.route('/change_password')
# def change_password():

#     return render_template('user/login_and_auth/change_password.html')


# @user.route('/dashboard')
# @login_required_l1
# @login_required_l2
# def dashboard():

#     username = session.get('username')
#     company_id = session.get('company_id')

#     try:
#         with engine.connect() as conn:
#             user = conn.execute(text("""
#             SELECT * FROM users 
#             WHERE company_id = :company_id 
#             AND (username = :username
#                 OR emp_email_id = :username
#                 OR emp_code = :username)
#         """), {'company_id': company_id, 'username': username}).fetchone()

#         user_data = {
#             'emp_code': user.emp_code,
#             'f_name': user.f_name,
#             'l_name': user.l_name,
#             'department': user.department,
#             'designation': user.designation

#         }
#         session['user_data'] = user_data

#     except:
#         pass


#     return render_template('user/dashboards/admin_dashboard.html', user_data=user_data)



