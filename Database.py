from Models import Base, User, Task
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://postgres:fort7859@localhost:5432/fastapi_db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session