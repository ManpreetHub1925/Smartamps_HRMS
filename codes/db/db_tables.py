from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime as dt
import uuid

Base = declarative_base()


# Masters

class MRole(Base):
    __tablename__ = 'm_role'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(105), unique=True, nullable=False)

class MDesignation(Base):
    __tablename__ = 'm_designation'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    designation_name = Column(String(255), unique=True, nullable=False)
    
class MPosition(Base):
    __tablename__ = 'm_position'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    position_name = Column(String(205), unique=True, nullable=False)
    
class MPayBand(Base):
    __tablename__ = 'm_payband'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    payband_name = Column(String(205), unique=True, nullable=False)
    payband_notice = Column(String(205), nullable=False)
    payband_salary_PM = Column(String(205), nullable=False)
    
class MDepartment(Base):
    __tablename__ = 'm_department'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(150), unique=True, nullable=False)
         
class MApplicationStage(Base):
    __tablename__ = 'm_application_stage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_name = Column(String(150), unique=True, nullable=False)
    stage_description = Column(Text, nullable=True)  
             
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(225), ForeignKey('employee.employee_code'), unique=True, nullable=False)
    username = Column(String(225), ForeignKey('employee.employee_code'), unique=True, nullable=False)
    password = Column(String(225), nullable=False)
    role = Column(Integer, ForeignKey('m_role.id'), nullable=False)
    profile_pic_url = Column(String(225), nullable=True)
    created_on = Column(DateTime, default=dt.utcnow, nullable=False)
    updated_on = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow, nullable=False)
    created_by = Column(String(225), ForeignKey('employee.employee_code'), nullable=False)
    updated_by = Column(String(225), ForeignKey('employee.employee_code'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

class Employee(Base):
    __tablename__ = 'employee'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_code = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)
    dob = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey('m_department.id'))  # Add ForeignKey if m_department defined
    designation_id = Column(Integer, ForeignKey('m_designation.id'))
    reporting_manager_id = Column(String(255), ForeignKey('employee.employee_code'), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    state = Column(String(150), nullable=True)
    country = Column(String(150), nullable=True)
    doj = Column(DateTime, default=dt.utcnow, nullable=False)
    created_by = Column(String(255), ForeignKey('employee.employee_code'), nullable=False)
    updated_by = Column(String(255), ForeignKey('employee.employee_code'), nullable=True)
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

class Jobs(Base):
    __tablename__ = 'Jobs'
    
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=False)
    job_location = Column(String(255), nullable=False)
    job_type = Column(Enum('Full-time', 'Part-time', 'Contract', 'Internship'), nullable=False)
    salary = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('m_department.id'))
    designation_id = Column(Integer, ForeignKey('m_designation.id'))
    created_by = Column(String(255), ForeignKey('users.username'), nullable=True)
    updated_by = Column(String(255), ForeignKey('users.username'), nullable=True)
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)
    updated_at = Column(DateTime, default=dt.utcnow, nullable=True)
    assigned_to = Column(String(255), ForeignKey('users.username'), nullable=True)
    assigned_by = Column(String(255), ForeignKey('users.username'), nullable=True)
    assigned_to_datetime = Column(DateTime, default=dt.utcnow, nullable=False)
    job_status = Column(Enum('Application Open', 'Application On-Hold', 'Application Archived','Application Rejected','Application Accepted','Application Assigned'), default='Position Open', nullable=True)

class JobsApplications(Base):
    __tablename__ = 'JobsApplications'
    application_id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('Jobs.job_id'), nullable=False)
    applicant_name = Column(String(255), nullable=False)
    applicant_email = Column(String(255), nullable=False)
    applicant_phone = Column(String(15), nullable=False)
    applicant_highest_qualification = Column(String(15), nullable=False)
    applicant_total_workEx = Column(String(15), nullable=False)
    applicant_relevent_workEx = Column(String(15), nullable=False)
    resume_url = Column(String(255), nullable=False)
    cover_letter = Column(Text, nullable=True)
    application_date = Column(DateTime, default=dt.utcnow, nullable=False)
    status = Column(String(225), default='Applied', nullable=False)
       
class JobsActivity(Base):
    __tablename__ = 'JobsActivity'
    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('Jobs.job_id'), nullable=False)
    activity_type = Column(Integer, ForeignKey('m_application_stage.id'), nullable=False)
    activity_description = Column(Integer, ForeignKey('m_application_stage.id'), nullable=False)
    activity_date = Column(DateTime, default=dt.utcnow, nullable=False)
    performed_by = Column(String(255), ForeignKey('users.username'), nullable=False)
 

class SystemConfig(Base):
    __tablename__ = 'system_config'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    license_key = Column(String(255), unique=True, nullable=False)
    domain_name = Column(String(255), nullable=False)
    is_setup_done = Column(Boolean, default=False, nullable=False)
    setup_date = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow, nullable=False)
    

    
