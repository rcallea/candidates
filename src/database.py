from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
"""
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL =  os.getenv('URL_DATABASE')
"""

DATABASE_URL = 'postgresql://postgres:5mG$1**8abcd@abc-jobs-postgres.cy4wad57lz7h.us-east-1.rds.amazonaws.com:5432/postgres'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()