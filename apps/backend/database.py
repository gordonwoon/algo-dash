# app/database.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import create_engine
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/dbname"

# SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# databases query builder
database = Database(DATABASE_URL)

Base = declarative_base()
