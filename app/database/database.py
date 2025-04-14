from sqlmodel import Session, create_engine

from app.core.config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(
    settings.DATABASE_URL, connect_args=connect_args, echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
