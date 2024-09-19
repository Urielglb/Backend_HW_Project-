from sqlmodel import Session, select
from app.models.user import User


def get_user_by_pin(session: Session, pin: str) -> User:
    return session.exec(select(User).where(User.pin == pin)).first()


def auth_user(session: Session, pin: str) -> User:
    return get_user_by_pin(session, pin)
