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

admin_bp = Blueprint('admin_bp', __name__)

engine = create_connections()

def have_access_(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role = session.get('role')  # Assuming role is stored in session
            if role not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('admin_bp.home'))  # Or wherever you want
            return f(*args, **kwargs)
        return wrapper
    return decorator

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('user_bp.login'))  
        return f(*args, **kwargs)
    return decorated_function


@require_login
@admin_bp.route('/admin/dashboard')
def home():
    return render_template('admin/dashboard.html')


@require_login
@have_access_(['Admin', 'Super_admin']) 
@admin_bp.route('/admin/register_company', methods=['GET', 'POST'])
def register_company():
    
    if request.method == 'POST':
        conn = engine.connect()
        try:
            with closing(conn.begin()):
                company_name = request.form.get('company_name')

                # 🔍 Check if company already exists
                if company_exists(company_name, conn):
                    flash('Company with this name already exists.', 'warning')
                    return redirect(url_for('admin.register_company'))

                # ✅ Continue with insert
                company_id = generate_company_id(company_name, conn)

                address = request.form.get('address')
                phone = request.form.get('phone')
                email = request.form.get('email')
                website = request.form.get('website')

                company_data = {
                    'company_id': company_id,
                    'company_name': company_name,
                    'address': address,
                    'phone': phone,
                    'email': email,
                    'website': website,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'status': 'active',
                }

                # ✅ Pass company_data as parameters
                conn.execute(text("""
                    INSERT INTO companies_details 
                    (company_id, company_name, address, phone, email, website, created_at, updated_at, status)
                    VALUES 
                    (:company_id, :company_name, :address, :phone, :email, :website, :created_at, :updated_at, :status)
                """), company_data)

                conn.commit()

                flash('Company details added successfully!', 'success')
                return redirect(url_for('user_bp.index'))

        except Exception as e:
            print("Exception occurred:", str(e))
            flash(f'Error adding company details: {str(e)}', 'error')
        finally:
            conn.close()
    return render_template('admin/register_company.html')


def company_exists(company_name, conn):
    query = text("SELECT 1 FROM companies_details WHERE LOWER(company_name) = LOWER(:company_name) LIMIT 1")
    result = conn.execute(query, {'company_name': company_name}).fetchone()
    return result is not None

def generate_company_id(company_name, conn):
    # Extract valid keyword from name
    words = re.findall(r'\b\w+\b', company_name.lower())
    ignore = {'private', 'limited', 'pvt', 'ltd', 'llp', 'inc', 'company', 'co', 'services'}
    filtered = [w for w in words if w not in ignore]

    if not filtered:
        raise ValueError("No valid company keyword found.")

    keyword = filtered[0].capitalize()
    prefix = f"SM_{keyword}_"

    # Find latest ID with same prefix
    query = text("SELECT company_id FROM companies_details WHERE company_id LIKE :prefix ORDER BY company_id DESC LIMIT 1")
    result = conn.execute(query, {'prefix': f"{prefix}%"})
    last_id = result.fetchone()

    if last_id:
        last_num = int(last_id[0].split('_')[-1])
        new_num = str(last_num + 1).zfill(5)
    else:
        new_num = "00001"

    return f"{prefix}{new_num}"



def generate_new_emp_code(conn, company_id, company_name):
    # Get prefix from company name (first 3 letters uppercased)
    prefix = company_name[:3].upper()
    code_prefix = f"{prefix}{company_id}_"

    # Get the latest emp_code for the company
    result = conn.execute(
        text("""
            SELECT emp_code FROM users 
            WHERE company_id = :company_id AND emp_code LIKE :code_prefix
            ORDER BY id DESC LIMIT 1
        """),
        {"company_id": company_id, "code_prefix": f"{code_prefix}%"}
    ).fetchone()

    if result:
        last_num = int(result[0].split("_")[1])
        new_num = last_num + 1
    else:
        new_num = 1

    return f"{code_prefix}{new_num:05d}" 


@require_login
@have_access_(['Admin', 'Super_admin']) 
@admin_bp.route('/admin/add_user/<company_id>', methods=['GET', 'POST'])
def add_user(company_id):
    if request.method == 'POST':
        conn = engine.connect()
        try:
            with closing(conn.begin()):
                company_name = conn.execute(
                    text("SELECT company_name FROM companies_details WHERE id = :id"),
                    {'id': company_id}
                ).scalar()

                emp_code = generate_new_emp_code(conn, company_id, company_name)
                f_name = request.form.get('first_name')
                l_name = request.form.get('last_name')  
                department = request.form.get('department')
                designation = request.form.get('designation')
                reporting_manager_l1 = request.form.get('reporting_manager_l1')
                reporting_manager_l2 = request.form.get('reporting_manager_l2')
                username = request.form.get('username')
                password = request.form.get('password') 
                emp_email_id = request.form.get('emp_email_id')
                emp_phone = request.form.get('emp_phone')
                emp_emr_phone = request.form.get('emp_emr_phone')
                role_id = request.form.get('role_id')
                role_name = request.form.get('role_name')

                if not company_exists(company_id, conn):
                    flash('Company with this ID does not exist.', 'warning')
                    return redirect(url_for('admin.add_user', company_id=company_id))

                # Check for existing username
                existing_user = conn.execute(
                    text("SELECT 1 FROM users WHERE LOWER(username) = LOWER(:username) AND company_id = :company_id"),
                    {'username': username, 'company_id': company_id}
                ).fetchone()

                if existing_user:
                    flash('Username already exists. Please choose a different one.', 'warning')
                    return redirect(url_for('admin.add_user', company_id=company_id))

                # Insert new user
                query = text(""" 
                    INSERT INTO users (company_id, emp_code, f_name, l_name, department, designation, 
                        reporting_manager_l1, reporting_manager_l2, username, password, 
                        emp_email_id, emp_phone, emp_emr_phone, role_id, role_name)
                    VALUES (:company_id, :emp_code, :f_name, :l_name, :department, :designation, 
                        :reporting_manager_l1, :reporting_manager_l2, :username, :password, 
                        :emp_email_id, :emp_phone, :emp_emr_phone, :role_id, :role_name)
                """)

                conn.execute(query, {
                    'company_id': company_id, 'emp_code': emp_code, 'f_name': f_name, 'l_name': l_name,
                    'department': department, 'designation': designation,
                    'reporting_manager_l1': reporting_manager_l1, 'reporting_manager_l2': reporting_manager_l2,
                    'username': username, 'password': password, 'emp_email_id': emp_email_id,
                    'emp_phone': emp_phone, 'emp_emr_phone': emp_emr_phone, 'role_id': role_id,
                    'role_name': role_name
                })

                flash('User details added successfully!', 'success')
                return render_template('admin/add_user_bp.html', company_id=company_id) # Adjust this route

        except Exception as e:
            print("Exception occurred:", str(e))
            flash(f'Error adding user details: {str(e)}', 'error')
        finally:
            conn.close()

    return render_template('admin/add_user_bp.html', company_id=company_id)





