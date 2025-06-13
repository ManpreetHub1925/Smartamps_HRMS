from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

def create_connection():
    server = '193.203.184.158'
    database = 'u759228348_SmartAmps'
    user_name = 'u759228348_SmartAmps'
    password = quote_plus('SmartAmps@123')  # Encodes @ to %40

    engine = create_engine(
        f"mysql+pymysql://{user_name}:{password}@{server}/{database}",
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
        echo=False
    )
    return engine

engine = create_connection()
