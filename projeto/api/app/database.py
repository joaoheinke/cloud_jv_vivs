import os
from dotenv import load_dotenv

load_dotenv()  # lê o .env montado em /app/.env

user   = os.getenv("POSTGRES_USER")
pwd    = os.getenv("POSTGRES_PASSWORD")
host   = os.getenv("POSTGRES_HOST")
port   = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{user}:{pwd}@{host}:{port}/{dbname}"

# resto igual
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
