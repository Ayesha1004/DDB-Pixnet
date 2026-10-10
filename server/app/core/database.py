import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
 
DB_USER = os.getenv("DB_USER", "pixnet") #(key, default)
DB_PASSWORD = os.getenv("DB_PASSWORD", "pixnet_ddb")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pixnet")
 
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() #base model, so we can use tables as classes 
def get_db():
    db = SessionLocal()
    try:
        yield db #requests will create new sessions
    finally:
        db.close()
