from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL') # DB URL

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base() 