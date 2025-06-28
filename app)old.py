from flask import Flask
import os
from datetime import timedelta
import secrets
from dotenv import load_dotenv
from codes.db.db import create_connections
from codes.db.migration import setup_database
import logging
from logging.handlers import RotatingFileHandler


engine = create_connections()

# Load environment variables from .env file
load_dotenv()

def create_app():
    """Application factory pattern for Flask"""
    app = Flask(__name__)
    
    # Configure basic application settings
    configure_app(app)
    
    # Initialize database connection and run migrations
    initialize_database(app)
    
    # Configure logging
    configure_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app

def configure_app(app):
    """Configure Flask application settings"""
    app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
    app.permanent_session_lifetime = timedelta(
        days=int(os.getenv("SESSION_LIFETIME_DAYS", 7))
    )
    
    # Additional configuration can be added here
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def initialize_database(app):
    """Initialize database connection and run migrations"""
    try:
        engine = create_connections()
        if not engine:
            app.logger.error("Failed to create database connection")
            raise RuntimeError("Database connection failed")
        
        # Setup database (migrations will only run once)
        setup_database(engine)
        
        # Store engine in app context for easy access
        app.config['engine'] = engine
        
    except Exception as e:
        app.logger.error(f"Database initialization failed: {str(e)}")
        raise

def configure_logging(app):
    """Configure application logging"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

def register_blueprints(app):
    """Register Flask blueprints"""
    from codes.setup.setup import setup
    from codes.frontend import frontend
    from codes.auth import auth
    
    app.register_blueprint(setup)
    app.register_blueprint(frontend)
    app.register_blueprint(auth)
    
    # Add more blueprints as needed

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv("APP_DEBUG", "True").lower() == "true"
    app.run(
        debug=debug_mode,
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "5000"))
    )