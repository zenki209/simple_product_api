from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

script_dir = Path(__file__).parent.absolute()
db_file = script_dir / 'product.db'

SQLALCHEMY_DB_URL = "r'sqlite:///"

engine = create_engine(r'sqlite:///c:\Users\koala\OneDrive\1.REPO\_SIDE_PROJECTS_REPO\fastAPI\project-with-sqlachemy\product.db',connect_args={
    "check_same_thread": False
})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

