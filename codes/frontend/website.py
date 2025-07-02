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

website_bp = Blueprint('website_bp', __name__)

engine = create_connections()

@website_bp.route('/')
def index():
    return render_template(
        'website/index.html'
    )


@website_bp.route('/about')
def about():
    return render_template(
        'website/about.html'
    )
    
    
@website_bp.route('/team')
def team():
    return render_template(
        'website/team.html'
    )
    
@website_bp.route('/why-us')
def why_us():
    return render_template(
        'website/why-us.html'
    )
    
    
@website_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Basic validation
        if not all([name, email, message]):
            flash('Please fill in all required fields', 'error')
        else:
            try:
                with engine.connect() as conn:
                    # Insert contact message into the database
                    query = text("""
                        INSERT INTO contact_messages (name, email, phone, subject, message, created_at) 
                        VALUES (:name, :email, :phone, :subject, :message, :created_at)
                    """)
                    conn.execute(query, {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'subject': subject,
                        'message': message,
                        'created_at': datetime.utcnow()
                    })
                    conn.commit()
                
                flash('Thank you for your message! We will contact you soon.', 'success')
                return redirect(url_for('website.contact'))
            
            except Exception as e:
                flash('An error occurred. Please try again later.', 'error')
    
    return render_template('website/contact.html')
    
    
@website_bp.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        country_code = request.form.get('country_code', '').strip()
        email_id = request.form.get('email', '').strip()
        mobile = request.form.get('phone', '').strip()
        company_name = request.form.get('company', '').strip()
        message = request.form.get('message', '').strip()
        employee_count = request.form.get('employees', '').strip()
        
        print(f'Name: {name}, Country Code: {country_code}, Mobile: {mobile}, Email: {email_id}, Company: {company_name}, Employees: {employee_count}, Message: {message}')
        
        try:
            with engine.begin() as conn:
                query = text("""
                    INSERT INTO demo_request (
                        name, country_code, mobile, email_id,
                        company_name, employee_count, message, created_at
                    ) VALUES (
                        :name, :country_code, :mobile, :email_id,
                        :company_name, :employee_count, :message, NOW()
                    )
                """)
                conn.execute(query, {
                    'name': name,
                    'country_code': country_code,
                    'mobile': mobile,
                    'email_id': email_id,
                    'company_name': company_name,
                    'employee_count': employee_count,
                    'message': message
                })

            flash('Thank you for your demo request! We will contact you soon.', 'success')
            return redirect(url_for('website.demo'))

        except Exception as e:
            print(f"[ERROR] Demo Request Failed: {e}")
            flash('Something went wrong. Please try again later.', 'error')
            return render_template('website/demo.html')

    return render_template('website/demo.html')
 
    
