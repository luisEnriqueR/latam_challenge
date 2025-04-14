from sqlmodel import SQLModel

from app.database.database import engine

# Model registration, do not remove this import
from app.models.user import User  # noqa: F401


def init_db():
    SQLModel.metadata.create_all(engine)
