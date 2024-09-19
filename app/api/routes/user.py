from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserRead, DepositRequest, WithdrawRequest
from app.core.db import get_session
from app.services.user import (
    deposit,
    withdraw,
    get_user_by_bank_account,
)

router = APIRouter()


@router.get("", response_model=list[UserRead])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


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
    deposit_request: DepositRequest, session: Session = Depends(get_session)
):
    user = deposit(session, deposit_request.bank_account, deposit_request.amount)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found or invalid bank account"
        )
    return user


@router.post("/withdraw/")
def withdraw_funds(
    withdraw_request: WithdrawRequest, session: Session = Depends(get_session)
):
    print(withdraw_request.pin)
    user = withdraw(session, withdraw_request.pin, withdraw_request.amount)
    if not user:
        raise HTTPException(
            status_code=400, detail="Insufficient funds or invalid account"
        )
    return user


@router.get("/by-bank-account/{bank_account}", response_model=UserRead)
def get_user_by_account(bank_account: str, session: Session = Depends(get_session)):
    user = get_user_by_bank_account(session, bank_account)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
