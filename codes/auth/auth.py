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

auth = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def loginRequire(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session and 'role' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember-me')

        if not username or not password:
            flash("Please enter both username and password.", "warning")
            return redirect(url_for('auth.login'))

        with engine.connect() as conn:
            query = text("SELECT * FROM v_employee_profile WHERE username = :username and user_is_active = 1")
            result = conn.execute(query, {"username": username}).mappings().fetchone()

        if not result:
            flash('Your Account is deactivated, please contact to you System Administrator.', 'danger')
            return redirect(request.referrer)
    
        if result:
            if password == result.password:  # ⚠️ Use hashing in production!
                # ✅ Properly set session
                session['username'] = result.username
                session['role'] = result.role_name.lower()
                session['employee_id'] = result.employee_code
                session['profile_pic'] = result.profile_pic_url

                session.permanent = True if remember_me else False

                flash("Login successful!", "success")
                role = result.role_name.lower()
                return redirect(url_for(f'{role}.dashboard'))
            else:
                flash("Invalid password. Please try again.", "danger")
                return redirect(url_for('auth.login'))
        else:
            flash("Username not found. Please check your username.", "danger")
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth.route('/logout')
@loginRequire
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.login'))


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email_id = request.form.get('email_id')
        employee_id = request.form.get('employee_id')
        if not email_id or not employee_id:
            flash("Please enter both email and employee ID.", "warning")
            return redirect(url_for('auth.forgot_password'))
        with engine.connect() as conn:
            query = text("SELECT * FROM v_employee_profile WHERE email = :email_id AND employee_code = :employee_id")
            result = conn.execute(query, {"email_id": email_id, "employee_id": employee_id}).mappings().fetchone()
        if result:
            new_generated_password = 'Welcome@123'
            
            with engine.connect() as conn:
                conn.execute(text(''' update users set password = :password where username = :username '''),{'password':new_generated_password, 'username': result.username})
                conn.commit()
            
            # Here you would typically send a password reset link to the user's email.
            print(f'''
                
                subject = "🔐 Password Reset Notification – SmartAmps HRMS"
                body = f"""\
                    Dear {result.first_name},

                    We received a request to reset your password for your SmartAmps HRMS account associated with this email address.

                    Your new login credentials are:

                    Username: {result.username}
                    Temporary Password: {new_generated_password}

                    ⚠️ Important: For your security, please log in using the above credentials and change your password immediately from your profile settings.

                    You can log in here: https://smartamps.in/login

                    If you did not request this change or believe this message was sent in error, please contact our support team immediately at support@smartamps.in.

                    Thank you,
                    SmartAmps HRMS Team
                    www.smartamps.in
                    """
            '''
            )
            
            flash("Password reset link has been sent to your email.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("No user found with the provided email and employee ID.", "danger")
            return redirect(url_for('auth.forgot_password'))
        
    return render_template('auth/forgot_password.html')


@auth.route('/2fa', methods=['GET', 'POST'])
@loginRequire
def two_factor_auth():
    if request.method == 'POST':
        code = request.form.get('code')
        if not code:
            flash("Please enter the 2FA code.", "warning")
            return redirect(url_for('auth.two_factor_auth'))
        # Here you would verify the 2FA code.
        # For demonstration, we'll assume the code is always valid.
        session['2fa_verified'] = True
        flash("2FA verification successful!", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/two_factor_auth.html')


@auth.route('/change_password', methods=['POST'])
@loginRequire
def change_password():
    
    username = session.get('username')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    if not current_password or not new_password:
        flash("Please fill in all fields.", "warning")
        return redirect(request.url)

    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE username = :username")
        result = conn.execute(query, {"username": username}).mappings().fetchone()

    if result:
        if new_password == result.password:
            flash("New password cannot be same as current password.", "warning")
            return redirect(request.url)

        with engine.begin() as conn:  # better for auto commit
            update_query = text("UPDATE users SET password = :new_password, updated_on = NOW(), updated_by = :username WHERE username = :username")
            conn.execute(update_query, {
                "new_password": new_password,
                "username": username
            })

        flash("Password changed successfully! Please log in again.", "success")
        logout()
        return redirect(url_for('auth.login'))

    else:
        flash("Current password is incorrect.", "danger")
        return redirect(request.url)


@auth.route('/active_2fector', methods=['POST'])
@loginRequire
def active_2fector():
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT 2_fector FROM users WHERE username = :username"),
            {'username': session['username']}
        ).mappings().fetchone()

        new_status = 0 if result['2_fector'] == 1 else 1

        conn.execute(
            text("UPDATE users SET 2_fector = :status WHERE username = :username"),
            {'status': new_status, 'username': session['username']}
        )

    flash(f"Two-Factor Authentication {'Disabled' if new_status == 0 else 'Enabled'}", 'success')
    return redirect(request.referrer or request.url)
    


@auth.route('/toggle_google_auth', methods=['POST'])
@loginRequire
def toggle_google_auth():
    username = session['username']

    with engine.begin() as conn:
        # Toggle value between 1 and 0
        conn.execute(text('''
            UPDATE users
            SET google_auth_enabled = CASE WHEN google_auth_enabled = 1 THEN 0 ELSE 1 END
            WHERE username = :username
        '''), {'username': username})

        # Get new value
        new_status = conn.execute(text('''
            SELECT google_auth_enabled FROM users WHERE username = :username
        '''), {'username': username}).scalar()

    flash(
        f"Google Authentication {'Enabled' if new_status == 1 else 'Disabled'}",
        "success"
    )
    return redirect(request.referrer or request.url)

@auth.route('/remove_phone', methods=['POST'])
@loginRequire
def remove_phone():
    username = session['username']
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE employee SET phone = '' WHERE employee_code = :username"),
            {"username": username}
        )
    flash("Phone number removed successfully.", "success")
    return redirect(request.referrer or request.url)

@auth.route('/remove_email', methods=['POST'])
@loginRequire
def remove_email():
    username = session['username']
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE employee SET email = '' WHERE employee_code = :username"),
            {"username": username}
        )
    flash("Email removed successfully.", "success")
    return redirect(request.referrer or request.url)


@auth.route('/change_phone', methods=['POST'])
@loginRequire
def change_phone():
    new_phone = request.form.get('new_phone')
    otp_input = request.form.get('otp_input')

    if not new_phone:
        flash("Phone number is required.", "warning")
        return redirect(request.referrer or request.url)

    # OPTIONAL: OTP verification logic placeholder
    # You can implement actual OTP storage/validation here
    if otp_input != "123456":  # Replace with real validation
        flash("Invalid OTP", "danger")
        return redirect(request.referrer or request.url)

    with engine.begin() as conn:
        conn.execute(
            text("UPDATE employee SET phone = :phone WHERE employee_code = :username"),
            {"phone": new_phone, "username": session['username']}
        )
    flash("Phone number updated successfully.", "success")
    return redirect(request.referrer or request.url)



@auth.route('/change_email', methods=['POST'])
@loginRequire
def change_email():
    new_email = request.form.get('new_email')
    otp_input = request.form.get('otp_input')

    if not new_email:
        flash("Email is required.", "warning")
        return redirect(request.referrer or request.url)

    # Replace with actual OTP verification logic
    if otp_input != "123456":
        flash("Invalid OTP", "danger")
        return redirect(request.referrer or request.url)

    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE employee 
                SET email = :email, email_verified = 1 
                WHERE employee_code = :username
            """),
            {"email": new_email, "username": session['username']}
        )

    flash("Email updated and verified successfully.", "success")
    return redirect(request.referrer or request.url)



@auth.route('/profile', methods=['GET', 'POST'])
@loginRequire
def profile():
    employee_id = session.get('employee_id')

    user_details = get_user_details(session['username'])

    if request.method == 'POST':
        email_id = request.form.get('email')
        phone_no = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        postal_code = request.form.get('pincode')

        # Handle profile picture upload
        profile_pic_file = request.files.get('profile_photo')
        filename = None

        if profile_pic_file and profile_pic_file.filename:
            # Generate unique filename
            file_name_text = f"{user_details.first_name}-{employee_id}"
            _, ext = os.path.splitext(profile_pic_file.filename)  # ✅ FIXED here
            filename = secure_filename(f"{file_name_text}{ext.lower()}")

            # Save location
            upload_dir = os.path.join('static', 'assets', 'img', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)

            save_path = os.path.join(upload_dir, filename)

            # Save the file
            profile_pic_file.save(save_path)
            
        # Update database
        with engine.begin() as conn:
            conn.execute(text(''' 
                UPDATE employee SET 
                    email = :email_id, 
                    phone = :phone_no, 
                    address = :address, 
                    city = :city,
                    state = :state, 
                    country = :country, 
                    pincode = :postal_code,
                    updated_by = :updated_by,
                    updated_at = NOW()
                WHERE employee_code = :employee_code
            '''), {
                'email_id': email_id,
                'phone_no': phone_no,
                'address': address,
                'city': city,
                'state': state,
                'country': country,
                'postal_code': postal_code,
                'employee_code': employee_id,
                'updated_by':employee_id
            })

            if filename:
                conn.execute(text('''
                    UPDATE users SET profile_pic_url = :profile_pic_url 
                    WHERE employee_id = :employee_id
                '''), {
                    'profile_pic_url': filename,
                    'employee_id': employee_id
                })

        flash("Profile updated successfully", "success")
        return redirect(url_for('auth.profile'))

    return render_template('user/pages/profile.html', user_details=user_details)



@auth.route('/lock_scereen', methods=['GET', 'POST'])
@loginRequire
def lock_screen():
    if request.method == 'POST':
        password = request.form.get('password')
        if not password:
            flash("Please enter your password to unlock.", "warning")
            return redirect(url_for('auth.lock_screen'))
        with engine.connect() as conn:
            query = text("SELECT * FROM users WHERE username = :username")
            result = conn.execute(query, {"username": session['username']}).fetchone()
        if result and check_password_hash(result['password'], password):
            flash("Screen unlocked successfully!", "success")
            return redirect(url_for('auth.profile'))
        else:
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('auth.lock_screen'))
    return render_template('auth/lock_screen.html')


@auth.route('/deactivate_account/<string:username>', methods=['POST'])
@loginRequire
def deactivate_account(username):
    if session.get('username') != username:
        flash("Unauthorized request.", "danger")
        return redirect(request.referrer or url_for('dashboard'))

    with engine.begin() as conn:
        conn.execute(
            text("UPDATE users SET is_active = 0 WHERE username = :username"),
            {'username': username}
        )

    session.clear()  # Log out user
    flash("Account has been deactivated.", "success")
    return redirect(request.referrer)



