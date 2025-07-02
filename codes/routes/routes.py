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


from codes.superadmin.superadmin import superadmin
from codes.admin.admin import admin
from codes.user.user import user

routes = Blueprint('routes', __name__)

def loginRequire(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session and 'role' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# # Dashabords Dropdown Routes

# @routes.route('/admin-dashbaord')
# @loginRequire
# def admin_dashbaord():
#     employee_id = session.get('username')
#     username = session.get('username')

#     user_details = get_user_details(username)

#     return redirect(url_for(admin.dashboard))

# @routes.route('/user-dashbaord')
# @loginRequire
# def user_dashbaord():
#     employee_id = session.get('username')
#     username = session.get('username')

#     user_details = get_user_details(username)

#     return redirect(url_for(user.dashboard))



# # Dropdown Superadmin Routes

# @routes.route('/superadmin-dashbaord')
# @loginRequire
# def superadmin_dashbaord():
#     employee_id = session.get('username')
#     username = session.get('username')

#     user_details = get_user_details(username)

#     return redirect(url_for(superadmin.dashboard))



@routes.route('/companies')
@loginRequire
def companies():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/dashboards/super_admin/companies.html' ,
                    user_details=user_details)


@routes.route('/subscriptions')
@loginRequire
def subscriptions():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/dashboards/super_admin/subscription.html' ,
                    user_details=user_details)



@routes.route('/packages-grid')
@loginRequire
def packages_grid():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/dashboards/super_admin/packages_grid.html' ,
                    user_details=user_details)


@routes.route('/packages-list')
@loginRequire
def packages_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/dashboards/super_admin/packages_list.html' ,
                    user_details=user_details)


@routes.route('/purchase-transaction')
@loginRequire
def purchase_transaction():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/dashboards/super_admin/purchase.html' ,
                    user_details=user_details)


# Dropdown Applications

@routes.route('/applications/chat')
@loginRequire
def application_chat():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/chats.html' ,
                    user_details=user_details)


@routes.route('/applications/calls/voice')
@loginRequire
def calls_voice():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/calls/voice_call.html' ,
                    user_details=user_details)


@routes.route('/applications/calls/video')
@loginRequire
def calls_video():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/calls/video_call.html' ,
                    user_details=user_details)


@routes.route('/applications/calls/outgoing')
@loginRequire
def outgoing_call():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/calls/outgoing_call.html' ,
                    user_details=user_details)


@routes.route('/applications/calls/incoming')
@loginRequire
def incoming_call():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/calls/incoming_call.html' ,
                    user_details=user_details)


@routes.route('/applications/calls/history')
@loginRequire
def calls_history():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/calls/call_history.html' ,
                    user_details=user_details)


@routes.route('/applications/calendar')
@loginRequire
def application_calendar():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/calendar.html' ,
                    user_details=user_details)


@routes.route('/applications/email/home')
@loginRequire
def application_email():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/email/emal_home.html' ,
                    user_details=user_details)


@routes.route('/applications/todo-grid')
@loginRequire
def application_todo_grid():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/todo.html' ,
                    user_details=user_details)


@routes.route('/applications/todo-list')
@loginRequire
def application_todo_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/todo_list.html' ,
                    user_details=user_details)


@routes.route('/applications/notes')
@loginRequire
def application_notes():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/applications/notes.html' ,
                    user_details=user_details)


# Employees Dropdown list

# Employees

@routes.route('/employees/employees-list')
@loginRequire
def employees_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/employees/employee_list.html' ,
                    user_details=user_details)


@routes.route('/employees/employees-grid')
@loginRequire
def employees_grid():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/employees/employee_grid.html' ,
                    user_details=user_details)


@routes.route('/employees/employees-details')
@loginRequire
def employees_details():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/employees/employee_details.html' ,
                    user_details=user_details)


@routes.route('/department-list')
@loginRequire
def department_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/employees/departments_list.html' ,
                    user_details=user_details)


@routes.route('/designations-list')
@loginRequire
def designations_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/employees/designations_list.html' ,
                    user_details=user_details)


@routes.route('/policies-list')
@loginRequire
def policies_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/employees/policies_list.html' ,
                    user_details=user_details)

# Tickets

@routes.route('/tickets-list')
@loginRequire
def tickets_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/tickets/tickets_list.html' ,
                    user_details=user_details)


@routes.route('/tickets-grid')
@loginRequire
def tickets_grid():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/tickets/tickets_grid.html' ,
                    user_details=user_details)


@routes.route('/tickets-details')
@loginRequire
def tickets_details():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/tickets/tickets_details.html' ,
                    user_details=user_details)


@routes.route('/holidays')
@loginRequire
def holidays():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/holidays.html' ,
                    user_details=user_details)


# Attendance Dropdown

# Leaves

@routes.route('/leaves-admin')
@loginRequire
def leaves_admin():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/leaves/leaves_admin.html' ,
                    user_details=user_details)


@routes.route('/leaves-employee')
@loginRequire
def leaves_employee():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/leaves/leaves_employee.html' ,
                    user_details=user_details)


@routes.route('/leaves/settings')
@loginRequire
def leaves_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/leaves/leaves_settings.html' ,
                    user_details=user_details)



@routes.route('/attendance-admin')
@loginRequire
def attendance_admin():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/attendance_admin.html' ,
                    user_details=user_details)


@routes.route('/attendance-employee')
@loginRequire
def attendance_employee():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/attendance_employee.html' ,
                    user_details=user_details)


@routes.route('/shift-and-schedule')
@loginRequire
def shift_and_schedule():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/shift_schedule.html' ,
                    user_details=user_details)


@routes.route('/timesheets')
@loginRequire
def timesheets():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/timesheets.html' ,
                    user_details=user_details)


@routes.route('/overtime')
@loginRequire
def overtime():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/attendance/overtime.html' ,
                    user_details=user_details)


# Performance Dropdown

@routes.route('/performance-indicator')
@loginRequire
def performance_indicator():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/performance/performance_indicator.html' ,
                    user_details=user_details)


@routes.route('/performance-review')
@loginRequire
def performance_review():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/performance/performance_review.html' ,
                    user_details=user_details)


@routes.route('/performance-appraisal')
@loginRequire
def performance_appraisal():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/performance/performance_appraisal.html' ,
                    user_details=user_details)


@routes.route('/performance-goal')
@loginRequire
def performance_goal():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/performance/performance_goal.html' ,
                    user_details=user_details)


@routes.route('/performance-type')
@loginRequire
def performance_type():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/performance/performance_type.html' ,
                    user_details=user_details)


# Training Dropdown

@routes.route('/training-list')
@loginRequire
def training_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/training/trainings.html' ,
                    user_details=user_details)


@routes.route('/training-type')
@loginRequire
def training_type():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/training/training_type.html' ,
                    user_details=user_details)


@routes.route('/trainers')
@loginRequire
def trainers():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/training/trainers.html' ,
                    user_details=user_details)


@routes.route('/promotion')
@loginRequire
def promotion():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/promotion.html' ,
                    user_details=user_details)


@routes.route('/resignation')
@loginRequire
def resignation():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/resignation.html' ,
                    user_details=user_details)


@routes.route('/termination')
@loginRequire
def termination():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/termination.html' ,
                    user_details=user_details)


# Recruitement Dropdown

# Jobs

@routes.route('/jobs-list')
@loginRequire
def jobs_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/recruitment/jobs/jobs_list.html' ,
                    user_details=user_details)


@routes.route('/jobs-grid')
@loginRequire
def jobs_grid():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/recruitment/jobs/jobs_grid.html' ,
                    user_details=user_details)


# Candidates

@routes.route('/candidate-list')
@loginRequire
def candidate_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/recruitment/candidates/candidate_list.html' ,
                    user_details=user_details)


@routes.route('/candidate-grid')
@loginRequire
def candidate_grid():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/recruitment/candidates/candidate_grid.html' ,
                    user_details=user_details)


@routes.route('/candidate-kanban')
@loginRequire
def candidate_kanban():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/recruitment/candidates/candidate_kanban.html' ,
                    user_details=user_details)


@routes.route('/candidate-refferals')
@loginRequire
def candidate_refferals():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/hrm/recruitment/candidates/refferals.html' ,
                    user_details=user_details)


# payroll dropdown

@routes.route('/payroll/employee-salary')
@loginRequire
def payroll_employee_salary():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/payroll/employee_salary.html' ,
                    user_details=user_details)


@routes.route('/payroll/employee-payslip')
@loginRequire
def payroll_employee_payslip():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/payroll/employee_payslip.html' ,
                    user_details=user_details)


# payroll Items

@routes.route('/payroll/addition')
@loginRequire
def payroll_addition():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/payroll/payroll_item/addition.html' ,
                    user_details=user_details)

@routes.route('/payroll/deductions')
@loginRequire
def payroll_deductions():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/payroll/payroll_item/deductions.html' ,
                    user_details=user_details)


@routes.route('/payroll/overtime')
@loginRequire
def payroll_overtime():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/payroll/payroll_item/overtime.html' ,
                    user_details=user_details)


# Administration

# Assets

@routes.route('/administration/assets')
@loginRequire
def administration_assets():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/assets.html' ,
                    user_details=user_details)


@routes.route('/administration/assets-list')
@loginRequire
def administration_assets_list():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/assets_list.html' ,
                    user_details=user_details)


# Help & Support

# Activities

@routes.route('/administration/activities')
@loginRequire
def administration_activities():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/activities.html' ,
                    user_details=user_details)


# Knowledge Base

@routes.route('/administration/knowledgebase-home')
@loginRequire
def knowledgebase_home():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/knowledge_bank/home.html' ,
                    user_details=user_details)


@routes.route('/administration/knowledgebase-details')
@loginRequire
def knowledgebase_details():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/knowledge_bank/details.html' ,
                    user_details=user_details)


# User Management

@routes.route('/administration/user-management')
@loginRequire
def user_management():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/user_management/users.html' ,
                    user_details=user_details)


@routes.route('/administration/roles-management')
@loginRequire
def roles_management():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/user_management/roles_manage.html' ,
                    user_details=user_details)


@routes.route('/administration/permission-management')
@loginRequire
def permission_management():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/administration/user_management/permission_manager.html' ,
                    user_details=user_details)


# Reports

@routes.route('/reports/expense-report')
@loginRequire
def report_expense_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/expenses-report.html' ,
                    user_details=user_details)


@routes.route('/reports/invoice-report')
@loginRequire
def report_invoice_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/invoice-report.html' ,
                    user_details=user_details)


@routes.route('/reports/payments-report')
@loginRequire
def report_payments_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/payments-report.html' ,
                    user_details=user_details)


@routes.route('/reports/projects-report')
@loginRequire
def report_projects_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/projects-report.html' ,
                    user_details=user_details)


@routes.route('/reports/task-report')
@loginRequire
def report_task_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/task-report.html' ,
                    user_details=user_details)


@routes.route('/reports/users-report')
@loginRequire
def report_users_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/users-report.html' ,
                    user_details=user_details)


@routes.route('/reports/employee-report')
@loginRequire
def report_employee_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/employee-report.html' ,
                    user_details=user_details)


@routes.route('/reports/payslip-report')
@loginRequire
def report_payslip_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/payslip-report.html' ,
                    user_details=user_details)


@routes.route('/reports/attendance-report')
@loginRequire
def report_attendance_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/attendance-report.html' ,
                    user_details=user_details)


@routes.route('/reports/leaves-report')
@loginRequire
def report_leaves_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/leaves-report.html' ,
                    user_details=user_details)


@routes.route('/reports/daily-report')
@loginRequire
def report_daily_report():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/reports/daily-report.html' ,
                    user_details=user_details)



# Settings Dropdown

# General Settings

@routes.route('/settings/profile')
@loginRequire
def profile_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/general_settings/profile-settings.html' ,
                    user_details=user_details)
    
    
    
@routes.route('/settings/notification')
@loginRequire
def notification_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/general_settings/notifications-settings.html' ,
                    user_details=user_details)


@routes.route('/settings/connected-apps')
@loginRequire
def connected_apps_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/general_settings/connected-apps-settings.html' ,
                    user_details=user_details)


# API Open-AI

@routes.route('/settings/open-ai')
@loginRequire
def connected_api_open_ai():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/ai-settings.html' ,
                    user_details=user_details)
    
    
# Ban-IP-Address

@routes.route('/settings/ban-ips')
@loginRequire
def ban_ips():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/ban-ip-address.html' ,
                    user_details=user_details)



# System Settings

@routes.route('/settings/email-settings')
@loginRequire
def email_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/system-settings/email-settings.html' ,
                    user_details=user_details)


@routes.route('/settings/email-templates')
@loginRequire
def email_templates():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/system-settings/email-templates.html' ,
                    user_details=user_details)
    
    
@routes.route('/settings/sms-settings')
@loginRequire
def sms_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/system-settings/sms-settings.html' ,
                    user_details=user_details)
    
    
    
@routes.route('/settings/sms-templates')
@loginRequire
def sms_templates():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/system-settings/sms-templates.html' ,
                    user_details=user_details)



@routes.route('/settings/cookies')
@loginRequire
def cookies_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/system-settings/GDPR-Cookies.html' ,
                    user_details=user_details)
    
    
@routes.route('/settings/maintenance-mode')
@loginRequire
def maintenance_mode_settings():
    employee_id = session.get('username')
    username = session.get('username')

    user_details = get_user_details(username)

    return render_template( 'user/settings/system-settings/maintenance-mode.html' ,
                    user_details=user_details)




# Quick Links

@routes.route('/employee-directory')
@loginRequire
def employee_directory():
    
    user_details = get_user_details(session['username'])
    
    if session['role'] not in ['admin', 'superadmin', 'manager']:
        flash('You are not authorised for this action', 'warning')
        return redirect(url_for(f'{session['role']}.dashboard'))  # or any fallback route

    with engine.connect() as conn:
        if session['role'] == 'manager':
            username = session['username']
            employees_list = conn.execute(
                text('SELECT * FROM v_employee_profile WHERE reporting_manager_name = :username'),
                {'username': username}
            ).mappings().fetchall()
        else:  # admin and superadmin
            employees_list = conn.execute(
                text('SELECT * FROM v_employee_profile')
            ).mappings().fetchall()

    return render_template('employee_directory.html', 
                           employees_list=employees_list, 
                           user_details=user_details)


@routes.route('/attendance-tracker')
@loginRequire
def attendance_tracker():

    user_details = get_user_details(session['username'])
    
    with engine.connect() as conn:
        
        username = session['username']
        attendance_calender = conn.execute(text(' select * from attendance where employee_id = :username'), {'username': username}).mappings().fetchall()
      

    return render_template('employee_directory.html', 
                           attendance_calender=attendance_calender, 
                           user_details=user_details)


@routes.route('/leaves-requests')
@loginRequire
def leaves_request():
    username = session['username']
    role = session['role']
    
    user_details = get_user_details(username)

    with engine.begin() as conn:
        if role in ['manager', 'employee', 'user']:
            leaves = conn.execute(
                text('''
                    SELECT * FROM leaves_requests
                    WHERE employee_id = :username OR review_by = :username
                '''), {'username': username}
            ).mappings().fetchall()
        else:
            leaves = conn.execute(
                text('SELECT * FROM leaves_requests')
            ).mappings().fetchall()

    return render_template('leaves_request.html', leaves=leaves, user_details=user_details)

    


