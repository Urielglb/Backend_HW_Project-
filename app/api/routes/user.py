from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models.user import UserCreate, UserRead
from app.core.db import get_session
from app.services.user import deposit, withdraw
from app.services.user import get_user_by_bank_account, update_user_balance

router = APIRouter()


@router.post("", response_model=UserRead)
def create_new_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.pin == user.pin)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/deposit/")
def deposit_funds(
    bank_account: str, amount: float, session: Session = Depends(get_session)
):
    user = deposit(session, bank_account, amount)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found or invalid bank account"
        )
    return user


@router.post("/withdraw/")
def withdraw_funds(
    bank_account: str, amount: float, session: Session = Depends(get_session)
):
    user = withdraw(session, bank_account, amount)
    if not user:
        raise HTTPException(
            status_code=400, detail="Insufficient funds or invalid account"
        )
    return user
