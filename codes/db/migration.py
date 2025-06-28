from sqlalchemy import inspect, text
from sqlalchemy.orm import sessionmaker
from .db_tables import *


def setup_database(engine):
    """Main setup function to be called from your app factory"""
    if not engine:
        raise RuntimeError("Database connection failed")
    
    # Create all tables first (if they don't exist)
    Base.metadata.create_all(engine)
    
    # Check if we need to run data migrations
    if not check_migration_status(engine):
        create_migration_history(engine)
        run_initial_migrations(engine)
    else:
        print("✅ Database already initialized - skipping data migration")
    
    return engine


def check_migration_status(engine):
    """Check if migrations have already been run"""
    with engine.connect() as conn:
        # First check if migration_history table exists
        inspector = inspect(engine)
        if 'migration_history' not in inspector.get_table_names():
            return False
            
        # Then check if initial migration was run
        result = conn.execute(text("""
            SELECT COUNT(*) FROM migration_history 
            WHERE migration_name = 'initial_setup'
        """)).scalar()
        
        return result > 0
    

def create_migration_history(engine):
    """Create a table to track migrations"""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS migration_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                migration_name VARCHAR(255) NOT NULL,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) NOT NULL
            )
        """))
        conn.commit()
            

def run_initial_migrations(engine):
    """Run initial database setup if needed"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("🏗️ Starting initial data migration...")
        
        # Insert only if empty
        if not session.query(MRole).first():
            session.add_all([
                MRole(role_name="Superadmin"),
                MRole(role_name="Admin"),
                MRole(role_name="Manager"),
                MRole(role_name="User")
            ])
            print("Inserted roles")

        if not session.query(MDesignation).first():
            session.add_all([
                MDesignation(designation_name="Superadmin"),
                MDesignation(designation_name="Admin"),
                MDesignation(designation_name="HOD"),
                MDesignation(designation_name="Manager")
            ])
            print("Inserted designations")

        if not session.query(MPosition).first():
            session.add_all([
                MPosition(position_name="Software Engineer"),
                MPosition(position_name="Senior Software Engineer"),
                MPosition(position_name="Project Manager"),
                MPosition(position_name="HR Manager"),
                MPosition(position_name="Data Scientist")
            ])
            print("Inserted positions")

        if not session.query(MPayBand).first():
            session.add_all([
                MPayBand(payband_name="Band G1", payband_notice="30 Days", payband_salary_PM="5000"),
                MPayBand(payband_name="Band B1", payband_notice="30 Days", payband_salary_PM="6000"),
                MPayBand(payband_name="Band B2", payband_notice="30 Days", payband_salary_PM="7000"),
                MPayBand(payband_name="Band B3", payband_notice="30 Days", payband_salary_PM="8000")
            ])
            print("Inserted paybands")

        if not session.query(MDepartment).first():
            session.add_all([
                MDepartment(department_name="Administrators"),
                MDepartment(department_name="Information Technology"),
                MDepartment(department_name="Human Resources"),
                MDepartment(department_name="Marketing"),
                MDepartment(department_name="Finance"),
                MDepartment(department_name="Sales")
            ])
            print("Inserted departments")
            
        if not session.query(MApplicationStage).first():
            session.add_all([
                # Initial Application Stages
                MApplicationStage(stage_name="Application Received", stage_description="Initial stage where applications are received."),
                MApplicationStage(stage_name="Referral Received", stage_description="Application received through an employee referral."),
                MApplicationStage(stage_name="Walk-in Application", stage_description="Application received from a walk-in candidate."),
                MApplicationStage(stage_name="Campus Drive", stage_description="Candidate sourced from a campus recruitment drive."),
                
                # Review and Assignment Stages
                MApplicationStage(stage_name="Application JD Review", stage_description="Reviewing the job description and requirements."),
                MApplicationStage(stage_name="Application Assigned", stage_description="Assignment of applications to recruiters."),
                
                # Sourcing and Posting Stages
                MApplicationStage(stage_name="Social Posting", stage_description="Job posted on social media platforms."),
                MApplicationStage(stage_name="Job Portal Posting", stage_description="Job posted on external job portals."),
                MApplicationStage(stage_name="Newspaper Advertisement", stage_description="Job advertised in newspapers."),
                MApplicationStage(stage_name="Application Posted on Website", stage_description="Job posted on company website."),
                
                # Screening Stages
                MApplicationStage(stage_name="Resume Screening", stage_description="Initial screening of candidate resumes."),
                MApplicationStage(stage_name="Screening", stage_description="Detailed screening of applications."),
                MApplicationStage(stage_name="Candidate Shortlisted", stage_description="Candidate approved for interview process."),
                
                # Candidate Contact Stages
                MApplicationStage(stage_name="Candidate Calling", stage_description="Phone screening with the candidate."),
                MApplicationStage(stage_name="Candidate Email", stage_description="Email communication with the candidate."),
                MApplicationStage(stage_name="Follow-up with Candidate", stage_description="Follow-up communication sent to the candidate."),
                MApplicationStage(stage_name="No Response from Candidate", stage_description="Candidate is unresponsive to calls/emails."),
                
                # Interview Stages
                MApplicationStage(stage_name="Interview Scheduled", stage_description="Interview scheduled with the candidate."),
                MApplicationStage(stage_name="Technical Assignment Sent", stage_description="Candidate sent a technical assignment."),
                MApplicationStage(stage_name="Technical Assignment Reviewed", stage_description="Technical assignment evaluation completed."),
                MApplicationStage(stage_name="First Round Interview", stage_description="First technical/functional interview round."),
                MApplicationStage(stage_name="Second Round Interview", stage_description="Second interview for deeper assessment."),
                MApplicationStage(stage_name="Third Round Interview", stage_description="Final technical/hiring round."),
                MApplicationStage(stage_name="Manager Round - L1", stage_description="First managerial level interview."),
                MApplicationStage(stage_name="Manager Round - L2", stage_description="Second managerial approval round."),
                MApplicationStage(stage_name="Interview Completed", stage_description="All interview rounds completed."),
                
                # Offer Stages
                MApplicationStage(stage_name="Salary Discussion", stage_description="Negotiation of salary expectations."),
                MApplicationStage(stage_name="Final HR Discussion", stage_description="Final discussion on offer terms."),
                MApplicationStage(stage_name="Offer Raised", stage_description="Formal job offer extended to candidate."),
                MApplicationStage(stage_name="Offer Accepted", stage_description="Candidate accepted the offer."),
                MApplicationStage(stage_name="Offer Rejected", stage_description="Candidate declined the offer."),
                
                # Verification Stages
                MApplicationStage(stage_name="Document Collection", stage_description="Gathering required candidate documents."),
                MApplicationStage(stage_name="Background Verification", stage_description="Background check in progress."),
                MApplicationStage(stage_name="Medical/Document Verification", stage_description="Medical and document verification."),
                
                # Pre-Joining Stages
                MApplicationStage(stage_name="Pre-Joining Follow-up", stage_description="Confirming candidate availability before joining."),
                MApplicationStage(stage_name="Joining Confirmed", stage_description="Candidate confirmed joining date."),
                
                # Joining and Onboarding Stages
                MApplicationStage(stage_name="Candidate Joined", stage_description="Candidate officially joined the organization."),
                MApplicationStage(stage_name="Welcome Email Sent", stage_description="Welcome email sent to new joiner."),
                MApplicationStage(stage_name="Buddy Assigned", stage_description="Onboarding buddy assigned to new hire."),
                MApplicationStage(stage_name="Onboarding", stage_description="Onboarding process initiated."),
                MApplicationStage(stage_name="Induction Process Initiated", stage_description="New employee induction started."),
                
                # Closing Stages
                MApplicationStage(stage_name="Application On Hold", stage_description="Application temporarily paused."),
                MApplicationStage(stage_name="Application Rejected", stage_description="Candidate rejected during process."),
                MApplicationStage(stage_name="Application Archived", stage_description="Application stored for records."),
                MApplicationStage(stage_name="Application Closed", stage_description="Position closed after hiring.")
            ])
            
            print("Inserted application stages")  
    
        # if not session.query(Employee).first():
        #     employee = Employee(
        #         employee_code="EMP0001", 
        #         first_name="Super", 
        #         last_name="Admin", 
        #         email="superadmin@hireamps.com", 
        #         phone="1234567890", 
        #         gender="Other", 
        #         dob="2000-01-01", 
        #         department_id=1, 
        #         designation_id=1,
        #         reporting_manager_id="EMP0001",  # No manager for superadmin
        #         address=None, city=None, pincode=None, 
        #         created_by="EMP0001",  # Will be valid after user is added
        #         updated_by="EMP0001",
        #         is_active=True
        #     )
        #     session.add(employee)
        #     session.flush()  # Ensure the insert is registered
            
        #     if not session.query(Users).first():
        #         user = Users(
        #             employee_id="EMP0001",
        #             username="EMP0001",
        #             password="superadmin123",
        #             role=1,
        #             profile_pic_url=None,
        #             created_by="EMP0001",
        #             updated_by="EMP0001",
        #             is_active=True
        #         )
        #         session.add(user)
                
        #     print("✅ Superadmin employee and user inserted successfully.")


        # Record the migration
        session.execute(text("""
            INSERT INTO migration_history 
            (migration_name, status) 
            VALUES ('initial_setup', 'completed')
        """))

        session.commit()
        print("🎉 Database initialization completed successfully")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error during data migration: {e}")
        raise
    finally:
        session.close()


