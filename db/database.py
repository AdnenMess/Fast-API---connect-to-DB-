import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import PostgresDsn

file = Path().cwd().parent / "SecondAPIProject" / "secret" / "conn.json"

with open(file, 'r') as f:
    data = json.load(f)
    user = data.get('user')
    password = data.get('password')
    host = data.get('host')
    port = data.get('port')


SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql",
    user=user,
    password=password,
    host=host,
    port=port,
    path=f"/{'FastAPI-Practice' or ''}")

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
