from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings


engine = create_engine(settings.DB_URL)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
