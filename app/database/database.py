import os

from sqlmodel import Session, create_engine

from app.core.config import settings

connect_args = {"check_same_thread": False}

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port
DB_NAME = os.getenv("DB_NAME")

if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

else:
    print("Database environment variables not fully set!")
    engine = None
engine = create_engine(
    settings.DATABASE_URL, connect_args=connect_args, echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
