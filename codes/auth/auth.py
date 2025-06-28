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

# from codes.queries import *

engine = create_connections()

auth_bp = Blueprint('auth_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def loginRequire(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session and 'role' not in session:
            # flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember-me')

        if username and password:
            with engine.connect() as conn:
                result = conn.execute(
                    text("""select * from v_employee_profile
                            WHERE username = :username"""),
                    {'username': username}
                )
                user = result.mappings().fetchone()
                                
                if user and user['password'] == password:
                    session.permanent = bool(remember)
                    session['username'] = user['username']
                    session['role'] = user['role_name'].lower()
                                            
                    if 'username' in session and 'role' in session:
                        flash("Login successful!", "success")
                        # print(session['role'])
                        return redirect(url_for(f"{session['role']}.dashboard"))

                    else:
                        flash("Unknown role, please contact support.", "danger")
                    
                else:
                    flash("Invalid username or password.", "danger")
        else:
            flash("Please enter both username and password.", "warning")

    return render_template('auth/login.html')


# @auth_bp.route('/logout')
# def logout():
#     session.clear()
#     flash("Logout successful!", "success")
#     return redirect(url_for('auth.login'))



@auth_bp.route('/forget_password', methods=['GET'])
def forget_password():
    return render_template('auth/forget_password.html')



# @auth_bp.route('/reset_password', methods=['GET','POST'])
# def reset_password():
#     username = session.get('username')
#     if not username:
#         flash("User not logged in!", "error")
#         return redirect(url_for('auth.login'))
    
#     # user_details = get_user_details()

#     with engine.begin() as conn:
#         result = conn.execute(
#             text('SELECT password FROM users WHERE username = :username'),
#             {'username': username}
#         )
#         user_record = result.fetchone()
#         if not user_record:
#             flash("User not found!", "error")
#             return redirect(url_for('auth.login'))

#         old_pass_db = user_record[0]

#         if request.method == 'POST':
#             old_password = request.form.get('old_password')
#             new_password = request.form.get('new_password')
#             confirm_password = request.form.get('confirm_password')

#             if old_password != old_pass_db:
#                 flash('Incorrect Old Password, please check again.', 'error')
#                 # return render_template('auth/reset_password.html', user_details=user_details)

#             if new_password != confirm_password:
#                 flash('New Password and Confirm Password do not match.', 'error')
#                 # return render_template('auth/reset_password.html', user_details=user_details)

#             conn.execute(
#                 text('UPDATE users SET password = :new_password WHERE username = :username'),
#                 {'new_password': confirm_password, 'username': username}
#             )
#             flash(f'Your password has been reset successfully!', 'success')
#             return redirect(url_for('auth.login'))

#     # return render_template('auth/reset_password.html', user_details=user_details)


# @auth_bp.route('/profile', methods=['GET', 'POST'])
# @loginRequire
# def profile():
#     username = session.get('username')
#     role = session.get('role')

#     UPLOAD_FOLDER = os.path.join('static', 'imgs', 'users')
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#     if request.method == 'POST':
#         dob = request.form.get('dob')
#         address = request.form.get('address')
#         city = request.form.get('city')
#         pincode = request.form.get('pincode')
#         phone_number = request.form.get('phone')
#         image_file = request.files.get('profile_image')

#         with engine.begin() as conn:
#             emp_row = conn.execute(
#                 text('SELECT employee_code FROM v_employee_profile WHERE username = :username'),
#                 {'username': username}
#             ).mappings().fetchone()

#             if emp_row:
#                 employee_code = emp_row['employee_code']

#                 # Prepare the update fields
#                 update_fields = {
#                     'dob': dob,
#                     'address': address,
#                     'city': city,
#                     'pincode': pincode,
#                     'phone': phone_number,
#                     'code': employee_code
#                 }

#                 # Handle image upload
#                 if image_file and allowed_file(image_file.filename):
#                     file_ext = image_file.filename.rsplit('.', 1)[1].lower()
#                     new_filename = f"{employee_code}_{username}_profile_img.{file_ext}"
#                     full_path = os.path.join(UPLOAD_FOLDER, new_filename)
#                     image_file.save(full_path)

#                     # Update user image path
#                     relative_path = os.path.join('imgs', 'users', new_filename)
#                     conn.execute(
#                         text('UPDATE users SET profile_pic_url = :img_path WHERE username = :username'),
#                         {'img_path': new_filename, 'username': username}
#                     )
#                 elif image_file:
#                     flash("Invalid image. Please upload PNG, JPG, or JPEG.", "danger")
#                     return redirect(url_for('auth.profile'))

#                 # Execute all updates for employee
#                 conn.execute(text('''
#                     UPDATE employee 
#                     SET dob = :dob, address = :address, city = :city, pincode = :pincode, phone = :phone 
#                     WHERE employee_code = :code
#                 '''), update_fields)

#                 flash("Profile updated successfully.", "success")
#             else:
#                 flash("Employee not found.", "danger")

#     # return render_template('auth/profile.html',
#                         #    user_details=get_user_details(),
#                         #    users_notification=get_notifications())


# @auth_bp.route('/master-manager', methods=['GET', 'POST'])
# @loginRequire
# def master_manager():
#     role = session.get('role')
#     if role not in ['admin', 'superadmin']:
#         flash('You are not authorized for this action.', 'error')
#         return redirect(url_for(f"{role}.dashboard"))

#     # user_details = get_user_details()

#     if request.method == 'POST':
#         form_type = request.form.get('form_type')

#         with engine.begin() as conn:
#             if form_type == 'department':
#                 department_name = request.form.get('department_name')
#                 if department_name:
#                     conn.execute(text('INSERT INTO m_department (department_name) VALUES (:name)'), {'name': department_name})
#                     flash('Department added successfully.', 'success')

#             elif form_type == 'designation':
#                 designation_name = request.form.get('designation_name')
#                 if designation_name:
#                     conn.execute(text('INSERT INTO m_designation (designation) VALUES (:name)'), {'name': designation_name})
#                     flash('Designation added successfully.', 'success')

#             elif form_type == 'role':
#                 role_name = request.form.get('role_name')
#                 if role_name:
#                     conn.execute(text('INSERT INTO m_role (role_name) VALUES (:name)'), {'name': role_name})
#                     flash('Role added successfully.', 'success')

#     # Fetch updated lists after possible insert
#     with engine.begin() as conn:
#         department_list = conn.execute(text('SELECT * FROM m_department')).mappings().fetchall()
#         designation_list = conn.execute(text('SELECT * FROM m_designation')).mappings().fetchall()
#         role_list = conn.execute(text('SELECT * FROM m_role')).mappings().fetchall()

#     # return render_template(
#     #     'setup/master_manage.html',
#     #     department_list=department_list,
#     #     designation_list=designation_list,
#     #     role_list=role_list,
#     #     user_details=user_details
#     # )


    

