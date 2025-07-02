import sqlalchemy
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECTION = os.getenv("DB_CONNECTION")


def create_connections():
    server = DB_HOST
    port = DB_PORT
    database = DB_DATABASE
    user_name = DB_USERNAME
    password = quote_plus(DB_PASSWORD) 

    try:
        connection_string = f"mysql+pymysql://{user_name}:{password}@{server}:{port}/{database}"
        engine = create_engine(connection_string, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Use text() wrapper
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
