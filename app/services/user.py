from sqlmodel import Session, select
from app.models.user import User


def get_user_by_bank_account(session: Session, bank_account: str) -> User:
    return session.exec(select(User).where(User.bank_account == bank_account)).first()


def get_user_by_pin(session: Session, pin: str) -> User:
    return session.exec(select(User).where(User.pin == pin)).first()


def update_user_balance(session: Session, user: User, new_balance: float) -> User:
    user.balance = new_balance
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def withdraw(session: Session, pin: str, amount: float) -> User:
    user = get_user_by_pin(session, pin)
    if user and user.balance >= amount:
        new_balance = user.balance - amount
        return update_user_balance(session, user, new_balance)
    return None


def deposit(session: Session, bank_account: str, amount: float) -> User:
    user = get_user_by_bank_account(session, bank_account)
    if user:
        new_balance = user.balance + amount
        return update_user_balance(session, user, new_balance)
    return None
