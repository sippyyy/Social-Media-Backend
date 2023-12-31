from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db on | defoff
    finally:
        db.close()
        
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Nguyenthuy209',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection was successfully')
#         break
#     except Exception as error:
#         print('Failed to connect to Database')
#         time.sleep(2)


